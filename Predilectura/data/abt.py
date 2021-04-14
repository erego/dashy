from dataclasses import dataclass
from pathlib import Path

from flask import current_app
import pandas as pd

from Predilectura import mongo


@dataclass
class ABT:
    features: dict


class ABTMongoDB(ABT):

    @staticmethod
    def get_events_stats(user_id):
        """
        Get statistics from events by user id
        :param user_id:
        :return: statistics from user id
        """
        # Get events data
        pipeline_events = [
            {
                u"$match": {
                    u"user_id": user_id
                }
            },
            {
                u"$group": {
                    u"_id": {
                        u"edition_id": u"$edition_id",
                        u"user_id": u"$user_id",
                        u"edition_language": u"$edition_language"
                    },
                    u"devices": {
                        u"$addToSet": u"$device"
                    },
                    u"versions": {
                        u"$addToSet": u"$version"
                    },
                    u"event_classes": {
                        u"$addToSet": u"$event_class"
                    },
                    u"event_objs": {
                        u"$addToSet": u"$event_obj"
                    },
                    u"event_types": {
                        u"$addToSet": u"$event_type"
                    },
                    u"chapters": {
                        u"$addToSet": u"$chapter_id"
                    }
                }
            }
        ]

        result_events = mongo.db.events.aggregate(
            pipeline_events
        )

        return result_events

    @staticmethod
    def get_readings_stats(user_id):
        """
        Get statistics from readings by user id
        :param user_id:
        :return: statistics from user id
        """
        # Get readings data
        pipeline_readings = [
            {
                u"$match": {
                    u"user_id": user_id
                }
            },
            {
                u"$group": {
                    u"_id": {
                        u"edition_id": u"$edition_id",
                        u"user_id": u"$user_id",
                        u"edition_language": u"$edition_language"
                    },
                    u"min_percent": {
                        u"$min": u"$percent"
                    },
                    u"max_percent": {
                        u"$max": u"$percent"
                    },
                    u"avg_percent": {
                        u"$avg": u"$percent"
                    },
                    u"max_words": {
                        u"$max": u"$words"
                    },
                    u"min_words": {
                        u"$min": u"$words"
                    },
                    u"avg_words": {
                        u"$avg": u"$words"
                    },
                    u"premium": {
                        u"$max": u"$premium"
                    },
                    u"devices": {
                        u"$addToSet": u"$device"
                    },
                    u"versions": {
                        u"$addToSet": u"$version"
                    },
                    u"chapters": {
                        u"$addToSet": u"$chapter_id"
                    }
                }
            }
        ]

        result_readings = mongo.db.readings.aggregate(
            pipeline_readings
        )

        return result_readings

    def create_ABT(self):

        # List of users
        # lst_users = [2074459, 2074562, 2074565]
        lst_users = mongo.db.readings.distinct("user_id")

        # Collection name
        collection_abt = mongo.db["abt"]

        # drop collection col1
        collection_abt.drop()

        for user in lst_users:

            # Get readings data by user
            result_readings = ABTMongoDB.get_readings_stats(user)
            user_data = []
            for result in result_readings:
                dict_user = {
                    "user_id": result["_id"]["user_id"],
                    "book": result["_id"]["edition_id"],
                    "language": result["_id"]["edition_language"]}

                if self.features["min_percent"] is True:
                    dict_user["min_percent"] = result["min_percent"]

                if self.features["max_percent"] is True:
                    dict_user["max_percent"] = result["max_percent"]

                if self.features["avg_percent"] is True:
                    dict_user["avg_percent"] = result["avg_percent"]

                if self.features["max_words"] is True:
                    dict_user["max_words"] = result["max_words"]

                if self.features["min_words"] is True:
                    dict_user["min_words"] = result["min_words"]

                if self.features["avg_words"] is True:
                    dict_user["avg_words"] = result["avg_words"]

                if self.features["premium"] is True:
                    dict_user["premium"] = result["premium"]

                if self.features["devices_readings"] is True:
                    dict_user["devices_readings"] = len(result["devices"])

                if self.features["versions_readings"] is True:
                    dict_user["versions_readings"] = len(result["versions"])

                if self.features["chapters_readings"] is True:
                    dict_user["chapters_readings"] = len(result["chapters"])

                if self.features["event_classes"] is True:
                    dict_user["event_classes"] = None

                if self.features["event_objs"] is True:
                    dict_user["event_objs"] = None

                if self.features["event_types"] is True:
                    dict_user["event_types"] = None

                if self.features["devices_events"] is True:
                    dict_user["devices_events"] = None

                if self.features["versions_events"] is True:
                    dict_user["versions_events"] = None

                if self.features["chapters_events"] is True:
                    dict_user["chapters_events"] = None

                user_data.append(dict_user)

            # Get events data by user
            result_events = ABTMongoDB.get_events_stats(user)

            for result in result_events:

                # Find this data in readings to update, if not create a new one
                element_found = None
                for element in user_data:
                    if element["user_id"] == result["_id"]["user_id"] \
                            and element["book"] == result["_id"]["edition_id"] \
                            and element["language"] == result["_id"]["edition_language"]:
                        element_found = element
                        break

                if element_found is None:
                    dict_user = {
                        "user_id": result["_id"]["user_id"],
                        "book": result["_id"]["edition_id"],
                        "language": result["_id"]["edition_language"]

                    }

                    if self.features["min_percent"] is True:
                        dict_user["min_percent"] = 0

                    if self.features["max_percent"] is True:
                        dict_user["max_percent"] = 0

                    if self.features["avg_percent"] is True:
                        dict_user["avg_percent"] = 0

                    if self.features["max_words"] is True:
                        dict_user["max_words"] = 0

                    if self.features["min_words"] is True:
                        dict_user["min_words"] = 0

                    if self.features["avg_words"] is True:
                        dict_user["avg_words"] = 0

                    if self.features["premium"] is True:
                        dict_user["premium"] = None

                    if self.features["devices_readings"] is True:
                        dict_user["devices_readings"] = None

                    if self.features["versions_readings"] is True:
                        dict_user["versions_readings"] = None

                    if self.features["chapters_readings"] is True:
                        dict_user["chapters_readings"] = None

                    if self.features["event_classes"] is True:
                        dict_user["event_classes"] = result["event_classes"]

                    if self.features["event_objs"] is True:
                        dict_user["event_objs"] = result["event_objs"]

                    if self.features["event_types"] is True:
                        dict_user["event_types"] = len(result["event_types"])

                    if self.features["devices_events"] is True:
                        dict_user["devices_events"] = len(result["devices"])

                    if self.features["versions_events"] is True:
                        dict_user["versions_events"] = len(result["versions"])

                    if self.features["chapters_events"] is True:
                        dict_user["chapters_events"] = len(result["chapters"])

                    user_data.append(dict_user)
                else:

                    if self.features["event_classes"] is True:
                        element_found["event_classes"] = result["event_classes"]

                    if self.features["event_objs"] is True:
                        element_found["event_objs"] = result["event_objs"]

                    if self.features["event_types"] is True:
                        element_found["event_types"] = len(result["event_types"])

                    if self.features["devices_events"] is True:
                        element_found["devices_events"] = len(result["devices"])

                    if self.features["versions_events"] is True:
                        element_found["versions_events"] = len(result["versions"])

                    if self.features["chapters_events"] is True:
                        element_found["chapters_events"] = len(result["chapters"])

            for element in user_data:
                collection_abt.insert(element)


class ABTPandas(ABT):

    @staticmethod
    def get_readings_stats(path_to_readings):
        """
        Return data frame with readings statistics
        :param path_to_readings: Path were readings csv is
        :return: data frame with readings statistics
        """
        readings = pd.read_csv(path_to_readings.as_posix())

        df_readings = readings.groupby(["user_id", "edition_id", "edition_language"], as_index=False)

        result_readings = df_readings.agg(min_words=('words', 'min'),
                                          max_words=('words', 'max'),
                                          avg_words=('words', 'mean'),
                                          min_percent=('percent', 'min'),
                                          max_percent=('percent', 'max'),
                                          avg_percent=('percent', 'mean'),
                                          premium=('premium', 'max'),
                                          devices_readings=('device', 'nunique'),
                                          versions_readings=('version', 'nunique'),
                                          chapters_readings=('chapter_id', 'nunique')
                                          )
        return result_readings

    @staticmethod
    def get_events_stats(path_to_events):
        """
        Return data frame with events statistics
        :param path_to_events: Path were events csv is
        :return: data frame with events statistics
        """

        events = pd.read_csv(path_to_events.as_posix())

        df_events = events.groupby(["user_id", "edition_id", "edition_language"], as_index=False)

        result_events = df_events.agg(event_classes=('event_class', 'unique'),
                                      event_objs=('event_obj_id', 'unique'),
                                      event_types=('event_type', 'nunique'),
                                      devices_events=('device', 'nunique'),
                                      versions_events=('version', 'nunique'),
                                      chapters_events=('chapter_id', 'nunique'))
        return result_events

    def create_ABT(self):

        path_to_readings = Path(current_app.root_path).joinpath("data", "readings.csv")

        result_readings = ABTPandas.get_readings_stats(path_to_readings)

        # Do a drop of not selected options
        columns_to_delete = []
        if self.features["min_percent"] is not True:
            columns_to_delete.append("min_percent")

        if self.features["max_percent"] is not True:
            columns_to_delete.append("max_percent")

        if self.features["avg_percent"] is not True:
            columns_to_delete.append("avg_percent")

        if self.features["max_words"] is not True:
            columns_to_delete.append("max_words")

        if self.features["min_words"] is not True:
            columns_to_delete.append("min_words")

        if self.features["avg_words"] is not True:
            columns_to_delete.append("avg_words")

        if self.features["premium"] is not True:
            columns_to_delete.append("premium")

        if self.features["devices_readings"] is not True:
            columns_to_delete.append("devices_readings")

        if self.features["versions_readings"] is not True:
            columns_to_delete.append("versions_readings")

        if self.features["chapters_readings"] is not True:
            columns_to_delete.append("chapters_readings")

        path_to_events = Path(current_app.root_path).joinpath("data", "events.csv")

        result_events = ABTPandas.get_events_stats(path_to_events)

        # Do a drop of not selected options
        if self.features["event_classes"] is not True:
            columns_to_delete.append("devices_readings")

        if self.features["event_objs"] is not True:
            columns_to_delete.append("devices_readings")

        if self.features["event_types"] is not True:
            columns_to_delete.append("devices_readings")

        if self.features["devices_events"] is not True:
            columns_to_delete.append("devices_events")

        if self.features["versions_events"] is not True:
            columns_to_delete.append("versions_events")

        if self.features["chapters_events"] is True:
            columns_to_delete.append("chapters_events")

        result = pd.merge(result_readings, result_events, on=['user_id', 'edition_id', "edition_language"], how='outer')
        result.drop(columns_to_delete, axis=1,  inplace=True)
        path_to_output = Path(current_app.root_path).joinpath("data", "abt.csv")

        if path_to_output.exists():
            path_to_output.unlink()

        result.to_csv(path_to_output.as_posix(), index=False)
