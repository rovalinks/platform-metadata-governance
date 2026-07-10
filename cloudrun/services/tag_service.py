from google.cloud import resourcemanager_v3
from google.api_core.exceptions import NotFound, AlreadyExists

from utils.logger import logger
from services.ownership import OwnershipService
import config
from utils.resource_names import to_full_resource_name

class TagService:
    """
    Applies Resource Manager Tags to resources.

    This service is used only for resources that do not
    support labels.
    """

    def __init__(self):
        self.tag_keys = resourcemanager_v3.TagKeysClient()
        self.tag_values = resourcemanager_v3.TagValuesClient()
        self.tag_bindings = resourcemanager_v3.TagBindingsClient()
        self.ownership = OwnershipService()

        #
        # In-memory caches.
        #
        self.tag_key_cache = {}
        self.tag_value_cache = {}

    def ensure_tag_key(
        self,
        short_name: str,
    ) -> str:
        """
        Returns the TagKey resource name.

        TagKeys are managed by Terraform.
        """

        parent = config.TAG_PARENT
        cache_key = short_name

        if cache_key in self.tag_key_cache:
            return self.tag_key_cache[cache_key]

        logger.info(
            "Looking up TagKey '%s'",
            short_name,
        )

        for key in self.tag_keys.list_tag_keys(
            parent=parent,
        ):

            if key.short_name == short_name:
                logger.info(
                    "Found TagKey %s",
                    key.name,
                )

                self.tag_key_cache[cache_key] = key.name
                return key.name

        raise RuntimeError(
            f"TagKey '{short_name}' was not found under "
            f"{parent}. Create it using Terraform."
        )

    def ensure_tag_value(
        self,
        tag_key_name: str,
        short_name: str,
    ) -> str:
        """
        Returns the TagValue resource name.

        Creates the TagValue if it does not already exist.
        """

        cache_key = (
            tag_key_name,
            short_name,
        )

        if cache_key in self.tag_value_cache:
            return self.tag_value_cache[cache_key]

        logger.info(
            "Looking up TagValue '%s' under %s",
            short_name,
            tag_key_name,
        )

        for value in self.tag_values.list_tag_values(
            parent=tag_key_name,
        ):

            if value.short_name == short_name:
                logger.info(
                    "Found TagValue %s",
                    value.name,
                )

                self.tag_value_cache[cache_key] = value.name
                return value.name

        logger.info(
            "Creating TagValue '%s'",
            short_name,
        )

        try:
            operation = self.tag_values.create_tag_value(
                tag_value=resourcemanager_v3.TagValue(
                    parent=tag_key_name,
                    short_name=short_name,
                    description=(
                        f"Platform managed value: "
                        f"{short_name}"
                    ),
                )
            )

            value = operation.result()

            logger.info(
                "Created TagValue %s",
                value.name,
            )
        except AlreadyExists:
            logger.info(
                "TagValue '%s' already exists.",
                short_name,
            )

            for value in self.tag_values.list_tag_values(
                parent=tag_key_name,
            ):
                if value.short_name == short_name:
                    break
        
        self.tag_value_cache[cache_key] = value.name
        return value.name

    def labels_to_tags(
        self,
        labels: dict,
    ) -> dict:
        """
        Converts registry labels into
        Resource Manager Tags.

        Registry format remains unchanged.
        """

        return labels.copy()

    def get_tags(
        self,
        resource_name: str,
    ) -> dict:
        """
        Returns the existing Resource Manager Tags
        currently bound to a resource.

        Result format:
        {
            "environment": "dev",
            "owner": "rks",
        }
        """

        tags = {}

        logger.info(
            "Reading TagBindings for %s",
            resource_name,
        )

        parent = to_full_resource_name( resource_name=resource_name,)

        for binding in self.tag_bindings.list_tag_bindings(
            parent=parent,
        ):
            try:
                #
                # binding.tag_value looks like:
                #
                # tagValues/456789012345
                #
                value = self.tag_values.get_tag_value(
                    name=binding.tag_value,
                )

                key = self.tag_keys.get_tag_key(
                    name=value.parent,
                )

                tags[key.short_name] = value.short_name
            except Exception:
                logger.warning(
                    "Skipping unreadable TagBinding %s",
                    binding.name,
                )

        logger.info(
            "Found %d TagBindings",
            len(tags),
        )

        return tags

    def _create_binding(
        self,
        resource_name: str,
        tag_value_name: str,
    ):
        """
        Creates a TagBinding if one does not already exist.
        """

        parent = to_full_resource_name( resource_name=resource_name,)

        #
        # Skip if already bound.
        #
        for binding in self.tag_bindings.list_tag_bindings(
            parent=parent,
        ):

            if binding.tag_value == tag_value_name:

                logger.info(
                    "TagBinding already exists."
                )

                return

        logger.info(
            "Creating TagBinding %s -> %s",
            parent,
            tag_value_name,
        )

        try:
            operation = self.tag_bindings.create_tag_binding(
                tag_binding=resourcemanager_v3.TagBinding(
                    parent=parent,
                    tag_value=tag_value_name,
                )
            )

            operation.result()

            logger.info(
                "TagBinding created."
            )
        except AlreadyExists:
            logger.info(
                "TagBinding already exists."
            )
            return

    def apply_tags(
        self,
        resource_name: str,
        desired_tags: dict,
        managed_tags: list[str],
    ) -> list[str]:
        """
        Applies Resource Manager Tags without
        modifying customer-managed tags.

        Returns the updated list of
        platform-managed tag keys.
        """

        existing_tags = self.get_tags(
            resource_name
        )

        final_tags = self.ownership.build(
            existing=existing_tags,
            desired=desired_tags,
            managed=managed_tags,
        )

        #
        # Remove platform tags that are no longer
        # present in the registry.
        #
        self.remove_tags(
            resource_name=resource_name,
            managed_tags=managed_tags,
            desired_tags=final_tags,
        )

        #
        # Apply desired tags.
        #
        for key, value in final_tags.items():

            tag_key = self.ensure_tag_key(
                key,
            )

            tag_value = self.ensure_tag_value(
                tag_key,
                value,
            )

            logger.info(
                "Binding %s=%s to %s",
                key,
                value,
                resource_name,
            )

            self._create_binding(
                resource_name=resource_name,
                tag_value_name=tag_value,
            )

        return self.ownership.managed_keys(
            existing=existing_tags,
            desired=desired_tags,
            managed=managed_tags,
        )

    def remove_tags(
        self,
        resource_name: str,
        managed_tags: list[str],
        desired_tags: dict,
    ):
        """
        Removes platform-managed tags that
        are no longer present in the registry.
        """

        parent = to_full_resource_name( resource_name=resource_name,)

        for binding in self.tag_bindings.list_tag_bindings(
            parent=parent,
        ):

            value = self.tag_values.get_tag_value(
                name=binding.tag_value,
            )

            key = self.tag_keys.get_tag_key(
                name=value.parent,
            )

            #
            # Customer-managed.
            #
            if key.short_name not in managed_tags:
                continue

            #
            # Still required.
            #
            if key.short_name in desired_tags:
                continue

            logger.info(
                "Removing TagBinding %s",
                binding.name,
            )

            operation = self.tag_bindings.delete_tag_binding(
                name=binding.name,
            )

            operation.result()