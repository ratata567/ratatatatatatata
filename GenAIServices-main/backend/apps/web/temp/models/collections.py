from pydantic import BaseModel
from peewee import *
from playhouse.shortcuts import model_to_dict
from typing import List, Union, Optional
import time
import logging

from utils.utils import decode_token
from utils.misc import get_gravatar_url

from apps.webui.internal.db import DB

import json

from config import SRC_LOG_LEVELS

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# Collections DB Schema
####################


class Collections(Model):
    collection_name = CharField()
    user_id = CharField()

    class Meta:
        database = DB


class CollectionsModel(BaseModel):
    collection_name: str
    user_id: str


####################
# Forms
####################


# class DocumentResponse(BaseModel):
#     collection_name: str
#     name: str
#     title: str
#     filename: str
#     content: Optional[dict] = None
#     user_id: str
#     timestamp: int  # timestamp in epoch


# class DocumentUpdateForm(BaseModel):
#     name: str
#     title: str


class CollectionsForm(DocumentUpdateForm):
    collection_name: str
    user_id: str


class CollectionsTable:
    def __init__(self, db):
        self.db = db
        self.db.create_tables([Collections])

    def insert_new_collection(
        self, user_id: str, collection_name:str
    ):
        document = CollectionsModel(
            **{
                "collection_name": collection_name,
                "user_id": user_id,
            }
        )

        collections = Collections.select().where((Collections.collection_name == collection_name) & (Collections.user_id == user_id))
        if len(collections) == 0:
            try:
                # print("Here6")
                result = Collections.create(**document.model_dump())
                # print(result)
                # print("########")
                if result:
                    return True
                else:
                    return False
            except:
                return False
        else:
            return False    

    

Collections = CollectionsTable(DB)
