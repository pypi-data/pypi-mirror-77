from typing import Union, List

from pyrasgo.connection import Connection
from pyrasgo.enums import ModelType
from pyrasgo.feature import Feature, FeatureList
from pyrasgo.member import Member
from pyrasgo.namespace import Namespace


class Model(Connection):
    """
    Stores all the features for a model
    """

    def __init__(self, api_object, **kwargs):
        self._namespace = Namespace(**api_object)
        super().__init__(**kwargs)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Model(id={self.id}, name={self.name})"

    def __getattr__(self, item):
        try:
            return self._namespace.__getattribute__(item)
        except KeyError:
            raise AttributeError(f"No attribute named {item}")

    @property
    def type(self):
        """
        Returns the model type of the model
        """
        return ModelType(self.__getattr__('type'))

    @property
    def features(self):
        """
        Returns the features within the model
        """
        return FeatureList([feature.to_dict() for feature in self.__getattr__('features')], api_key=self._api_key)

    @features.setter
    def features(self, features: Union[List[Feature], FeatureList]):
        # Update the namespace
        self._namespace.__setattr__('features', [Namespace(**feature.to_dict()) for feature in self.features + features])

    def get(self):
        """
        Updates the Model object's attributes from the API
        """
        self._namespace = Namespace(**self._get(f"/models/{self.id}").json())

    def get_author(self):
        """
        Returns the full author object of the model (including credentials)
        """
        return Member(self.author.to_dict())

    def add_feature(self, feature: Feature):
        self.features = [feature]
        self._patch(f"/models/{self.id}", _json=self._namespace.to_dict())

    def add_features(self, features: FeatureList):
        self.features = features
        self._patch(f"/models/{self.id}", _json=self._namespace.to_dict())


    def generate_training_data(self):
        self._get(f"/models/{self.id}/train")

    def snowflake_table_metadata(self, creds):
        metadata = {
            "database": creds.get("database", "rasgoalpha"),
            "schema": creds.get("schema", "public"),
            "table": self._snowflake_table_name(),
        }
        return metadata

    def _snowflake_table_name(self):
        table_name = self.dataTableName
        if table_name is None:
            raise ValueError("No table found for model '{}'".format(self.id))
        return table_name
