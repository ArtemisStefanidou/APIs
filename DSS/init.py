from pymongo import MongoClient
from bson.json_util import dumps

client = MongoClient("mongodb://mongodb:27017")
db = client["kafka_db"]
client.drop_database("dock-mongo_mongodb_1")


def init_COPs():
    COPS = [
		{
			"id": "1",
			"message_type": "COP",
			"threat_name": "Sudden change in SoG",
			"threat_description": "Sudden change in SoG",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"id": "2",
			"message_type": "COP",
			"threat_name": "Abrupt change in CoG",
			"threat_description": "Abrupt change in CoG",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"id": "3",
			"message_type": "COP",
			"threat_name": "Suspicious anchoring",
			"threat_description": "Suspicious anchoring",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"id": "4",
			"message_type": "COP",
			"threat_name": "Dark vessel detected",
			"threat_description": "Dark vessel detected",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"id": "5",
			"message_type": "COP",
			"threat_name": "Vessels rendezvous",
			"threat_description": "Detect a rendezvous of two or more vessels",
			"steps": [
				{
					"no": 1,
					"description": "Call the involved vessels."
				},
				{
					"no": 2,
					"description": "Send a UAV."
				},
				{
					"no": 3,
					"description": "Send the coastguard. Activate emergency response teams."
				}
			]
		},
		{
			"id": "6",
			"message_type": "COP",
			"threat_name": "Vessel approaching shoreline",
			"threat_description": "Detected a vessel approaching the shoreline",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Deploy pilot boats / tug boats"
				},
				{
					"no": 3,
					"description": "Send the coastguard. Activate emergency response teams."
				}
			]
		},
		{
			"id": "7",
			"message_type": "COP",
			"threat_name": "Vessel at shore",
			"threat_description": "Detected a vessel at shore",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Send a UAV"
				},
				{
					"no": 3,
					"description": "Activate port and land emergency response teams (coastguard/police)."
				}
			]
		},
		{
			"id": "8",
			"message_type": "COP",
			"threat_name": "People detected on deck",
			"threat_description": "Detected people on the deck",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Alert nearby vessels"
				},
				{
					"no": 3,
					"description": "Deploy pilot boats / tug boats"
				},
				{
					"no": 4,
					"description": "Send the coastguard. Activate emergency response teams."
				}
			]
		},
		{
			"id": "9",
			"message_type": "COP",
			"threat_name": "People left vessel coming ashore",
			"threat_description": "Track people coming ashore from the vessel",
			"steps": [
				{
					"no": 1,
					"description": "Send the police. Activate land emergency response teams."
				},
				{
					"no": 2,
					"description": "Send a UAV."
				}
			]
		},
		{
			"id": "10",
			"message_type": "COP",
			"threat_name": "Navigational status changed",
			"threat_description": "Detect change in navigational status",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Inform the responsible authority"
				},
				{
					"no": 3,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 4,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"id": "11",
			"message_type": "COP",
			"threat_name": "Check if AIS required",
			"threat_description": "Check if AIS required",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"id": "12",
			"message_type": "COP",
			"threat_name": "AIS spoofing detected",
			"threat_description": "AIS spoofing detected",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"id": "13",
			"message_type": "COP",
			"threat_name": "Detect vessel entering/leaving area shutting down its AIS",
			"threat_description": "Detect vessel entering/leaving area shutting down its AIS",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"id": "14",
			"message_type": "COP",
			"threat_name": "Vessel in distress",
			"threat_description": "Detected a vessel in distress",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				},
				{
					"no": 2,
					"description": "Inform the responsible authority"
				},
				{
					"no": 3,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 4,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"id": "15",
			"message_type": "COP",
			"threat_name": "Oil spill detected",
			"threat_description": "Oil spill detected",
			"steps": [
				{
					"no": 1,
					"description": "Call the responsible authority"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets"
				}
			]
		},
		{
			"id": "16",
			"message_type": "COP",
			"threat_name": "Vessel on collision course",
			"threat_description": "Detect if a vessel is on a collision course with another or with coast",
			"steps": [
				{
					"no": 1,
					"description": "Inform the proper authorities (MRCC)"
				}
			]
		},
		{
			"id": "17",
			"message_type": "COP",
			"threat_name": "People split into groups",
			"threat_description": "Track if the group of people landed from the vessel is divided into two or more groups",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land and sea"
				}
			]
		},
		{
			"id": "18",
			"message_type": "COP",
			"threat_name": "People boarded a vehicle",
			"threat_description": "Detected people walking on foot picked up by a vehicle",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land"
				}
			]
		}
	]
    collection = db["COPs"]
    collection.insert_many(COPS)

def init_alerts():
	alerts = [
		{
			"track_id": "1",
			"message_type": "alert",
			"threat_name": "Sudden change in SoG",
			"threat_description": "Sudden change in SOG",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"track_id": "2",
			"message_type": "alert",
			"threat_name": "Abrupt change in CoG",
			"threat_description": "Abrupt change in COG",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"track_id": "3",
			"message_type": "alert",
			"threat_name": "Suspicious anchoring",
			"threat_description": "Suspicious anchoring",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"track_id": "4",
			"message_type": "alert",
			"threat_name": "Dark vessel detected",
			"threat_description": "Dark vessel detected",
			"steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Deploy a UAV/EURMARS asset"
				}
			]
		},
		{
			"track_id": "5",
			"message_type": "alert",
			"threat_name": "Detect a rendezvous of two or more vessels",
			"threat_description": "Detect a rendezvous of two or more vessels",
			"steps": [
				{
					"no": 1,
					"description": "Call the involved vessels.",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Send a UAV.",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send the coastguard. Activate emergency response teams",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the involved vessels"
				}
			]
		},
		{
			"track_id": "6",
			"message_type": "alert",
			"threat_name": "Vessel approaching shoreline",
			"threat_description": "Detected a vessel approaching the shoreline",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy pilot boats / tug boats",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send the coastguard. Activate emergency response teams.",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"track_id": "7",
			"message_type": "alert",
			"threat_name": "Vessel at shore",
			"threat_description": "Detected a vessel at shore",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Send a UAV",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Activate port and land emergency response teams (coastguard/police).",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"track_id": "8",
			"message_type": "alert",
			"threat_name": "People detected on deck",
			"threat_description": "Detected people on the deck",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Alert nearby vessels",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Deploy pilot boats / tug boats",
					"status": "Not initialized"
				},
				{
					"no": 4,
					"description": "Send the coastguard. Activate emergency response teams.",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"track_id": "9",
			"message_type": "alert",
			"threat_name": "People left vessel coming ashore",
			"threat_description": "Track people coming ashore from the vessel",
			"steps": [
				{
					"no": 1,
					"description": "Send the police. Activate land emergency response teams.",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Send a UAV.",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Send the police. Activate land emergency response teams."
				}
			]
		},
		{
			"track_id": "10",
			"message_type": "alert",
			"threat_name": "Navigational status changed",
			"threat_description": "Detect change in navigational status",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Inform the responsible authority",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 4,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"track_id": "11",
			"message_type": "alert",
			"threat_name": "Check if AIS required",
			"threat_description": "Check if AIS required",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"track_id": "12",
			"message_type": "alert",
			"threat_name": "AIS spoofing detected",
			"threat_description": "AIS spoofing detected",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"track_id": "13",
			"message_type": "alert",
			"threat_name": "Detect vessel entering/leaving area shutting down its AIS",
			"threat_description": "Detect vessel entering/leaving area shutting down its AIS",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"track_id": "14",
			"message_type": "alert",
			"threat_name": "Vessel in distress",
			"threat_description": "Detect vessel in distress",
			"steps": [
				{
					"no": 1,
					"description": "Call the vessel",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Inform the responsible authority",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 4,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the vessel"
				}
			]
		},
		{
			"track_id": "15",
			"message_type": "alert",
			"threat_name": "Oil spill detected",
			"threat_description": "Oil spill detected",
			"steps": [
				{
					"no": 1,
					"description": "Call the responsible authority",
					"status": "Not initialized"
				},
				{
					"no": 2,
					"description": "Deploy a UAV/EURMARS asset",
					"status": "Not initialized"
				},
				{
					"no": 3,
					"description": "Send naval responsible assets",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Call the responsible authority"
				}
			]
		},
		{
			"track_id": "16",
			"message_type": "alert",
			"threat_name": "Vessel on collision course",
			"threat_description": "Detect if a vessel is on a collision course with another or with coast",
			"steps": [
				{
					"no": 1,
					"description": "Inform the proper authorities (MRCC)",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Inform the proper authorities (MRCC)"
				}
			]
		},
		{
			"track_id": "17",
			"message_type": "alert",
			"threat_name": "People split into groups",
			"threat_description": "Track if the group of people landed from the vessel is divided into two or more groups",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land and sea",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Interception on land and sea"
				}
			]
		},
		{
			"track_id": "18",
			"message_type": "alert",
			"threat_name": "People boarded a vehicle",
			"threat_description": "Detected people walking on foot picked up by a vehicle",
			"steps": [
				{
					"no": 1,
					"description": "Interception on land",
					"status": "Not initialized"
				}
			],
			"rec_steps": [
				{
					"no": 1,
					"description": "Interception on land"
				}
			]
		}
	]
	collection = db["alerts"]
	collection.insert_many(alerts)

    
if __name__ == '__main__':
	cops = db["COPs"]
	cops.drop()
	alerts = db["alerts"]
	alerts.drop()
	init_COPs()
	init_alerts()
