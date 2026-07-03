from classifiers.compute import (
    ComputeClassifier,
)


class ClassificationEngine:

    def __init__(self):

        self.classifiers = [

            ComputeClassifier(),

        ]

    def classify(
        self,
        event,
    ):

        for classifier in self.classifiers:

            if classifier.supports(
                event
            ):
                return classifier.classify(
                    event
                )

        return None