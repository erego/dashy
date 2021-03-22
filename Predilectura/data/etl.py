"""
Extract transform and load data from mongodb to generate the analytics base data
"""

from wsgi import mongo


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
                }
            }
        }
    ]

    result_readings = mongo.db.readings.aggregate(
        pipeline_readings
    )

    return result_readings


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
                }
            }
        }
    ]

    result_readings = mongo.db.readings.aggregate(
        pipeline_readings
    )

    return result_readings
