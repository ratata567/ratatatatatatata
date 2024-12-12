from pydantic import BaseModel, ConfigDict
from peewee import *
from playhouse.shortcuts import model_to_dict
from sqlalchemy import PrimaryKeyConstraint, String, Column, BigInteger, Text
from typing import List, Union, Optional
import time
import logging

from utils.utils import decode_token
from utils.misc import get_gravatar_url



from apps.webui.internal.db import Base, JSONField, Session, get_db
# from apps.rag.main import store_docs_in_vector_db, delete_docs_from_vector_db, get_loader

import json

from config import (
    SRC_LOG_LEVELS,
    UPLOAD_DIR,
);

log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

####################
# Documents db Schema
####################


class Document(Base):
    __tablename__ = "document"
    __table_args__ = (
        PrimaryKeyConstraint('name', 'user_id'),
    )

    collection_name = Column(String)
    name = Column(String)
    title = Column(Text)
    filename = Column(Text)
    content = Column(Text, nullable=True)
    user_id = Column(String)
    timestamp = Column(BigInteger)
    vector_ids = Column(Text)


class DocumentModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    collection_name: str
    name: str
    title: str
    filename: str
    content: Optional[str] = None
    user_id: str
    timestamp: int  # timestamp in epoch
    vector_ids: str


####################
# Forms
####################


class DocumentResponse(BaseModel):
    collection_name: str
    name: str
    title: str
    filename: str
    content: Optional[dict] = None
    user_id: str
    timestamp: int  # timestamp in epoch
    vector_ids: str


class DocumentUpdateForm(BaseModel):
    name: str
    title: str
    collection_name: str
    vector_ids: str


class DocumentForm(DocumentUpdateForm):
    collection_name: str
    filename: str
    content: Optional[str] = None
    vector_ids: str


class DocumentsTable:

    def insert_new_doc(
        self, user_id: str, form_data: DocumentForm
    ) -> Optional[DocumentModel]:
        with get_db() as db:

            document = DocumentModel(
                **{
                    **form_data.model_dump(),
                    "user_id": user_id,
                    "timestamp": int(time.time()),
                }
            )

            try:
                result = Document(**document.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)
                if result:
                    return DocumentModel.model_validate(result)
                else:
                    return None
            except:
                return None
    

    # Old function used to retrieve doc only by name not user
    def get_doc_by_name(self, name: str) -> Optional[DocumentModel]:
        try:
            with get_db() as db:

                document = db.query(Document).filter_by(name=name).first()
                return DocumentModel.model_validate(document) if document else None
        except:
            return None
    
    def get_doc_by_name_and_user(self, name: str, user_id: str) -> Optional[DocumentModel]:
        try:
            with get_db() as db:

                document = db.query(Document).filter_by(name=name, user_id=user_id).first()
                print("Here5")
                # print(len(document))
                if document:
                    # print(document)
                    # print("########")
                    result =  DocumentModel.model_validate(document) if document else None
                    # print(result)
                    # print("########")
                    return result
                    
                else:
                    return None
                   
        except Exception as e:
            print(e)
            return None
    
    def get_docs_by_user_and_collection(self, user_id: str, collection_name: str) -> int:
        try:
            with get_db() as db:

                document = db.query(Document).filter_by(collection_name=collection_name, user_id=user_id).all()
                # print("Here5")
                # print(len(document))
                if document == None:
                    return None
                else:
                    return len(document)
        except:
            return None

    # Old function used to retrieve all docs for display
    def get_docs(self) -> List[DocumentModel]:
        with get_db() as db:

            return [
                DocumentModel.model_validate(doc) for doc in db.query(Document).all()
            ]
    
    def get_docs_of_user(self, user_id: str) -> List[DocumentModel]:
        try: 
            with get_db() as db:

                docs = [
                    DocumentModel.model_validate(doc) for doc in db.query(Document).filter_by(user_id=user_id).all()
                ]
                # print(docs)
                return docs

        except Exception as e:
            print(e)
            return None
        

    # Old function used to update documents only based on name
    def update_doc_by_name(
        self, name: str, form_data: DocumentUpdateForm
    ) -> Optional[DocumentModel]:
        try:
            with get_db() as db:

                db.query(Document).filter_by(name=name).update(
                    {
                        "title": form_data.title,
                        "name": form_data.name,
                        "timestamp": int(time.time()),
                    }
                )
                db.commit()
                return self.get_doc_by_name(form_data.name)
        except Exception as e:
            log.exception(e)
            return None
    

    def update_doc_by_name_and_user(
        self, name: str, user_id: str, form_data: DocumentUpdateForm
    ) -> Optional[DocumentModel]:
        try:
            with get_db() as db:
                # print(form_data)

                # doc_to_be_updated = DocumentModel.model_validate(db.query(Document).filter_by(name=name, user_id=user_id).first())
                # old_collection = doc_to_be_updated.collection_name
                # vector_ids = doc_to_be_updated.vector_ids

                # if form_data.collection_name != old_collection:
                #     filename =  doc_to_be_updated.filename

                #     file_path = f"{UPLOAD_DIR}/{filename}"

                #     mime = magic.Magic(mime=True)
                #     mime_type = mime.from_file(file_path)

                #     f = open(file_path, "rb")
                #     f.close()

                #     loader, known_type = get_loader(filename, mime_type, file_path)
                #     data = loader.load()

                #     result = store_docs_in_vector_db(data, form_data.collection_name)

                #     delete_docs_from_vector_db(old_collection, vector_ids)

                #     vector_ids = result

                db.query(Document).filter_by(name=name, user_id=user_id).update(
                    {
                        "title": form_data.title,
                        "name": form_data.name,
                        "collection_name": form_data.collection_name,
                        "timestamp": int(time.time()),
                        "vector_ids": form_data.vector_ids
                    }
                )
                db.commit()
                return self.get_doc_by_name(form_data.name)
        except Exception as e:
            log.exception(e)
            return None

    def update_doc_content_by_name(
        self, name: str, updated: dict
    ) -> Optional[DocumentModel]:
        try:
            doc = self.get_doc_by_name(name)
            doc_content = json.loads(doc.content if doc.content else "{}")
            doc_content = {**doc_content, **updated}

            with get_db() as db:

                db.query(Document).filter_by(name=name).update(
                    {
                        "content": json.dumps(doc_content),
                        "timestamp": int(time.time()),
                    }
                )
                db.commit()
                return self.get_doc_by_name(name)
        except Exception as e:
            log.exception(e)
            return None

    def update_doc_content_by_name_and_user(
        self, name: str, user_id: str, updated: dict
    ) -> Optional[DocumentModel]:
        try:
            doc = self.get_doc_by_name(name)
            doc_content = json.loads(doc.content if doc.content else "{}")
            doc_content = {**doc_content, **updated}

            with get_db() as db:

                db.query(Document).filter_by(name=name, user_id=user_id).update(
                    {
                        "content": json.dumps(doc_content),
                        "timestamp": int(time.time()),
                    }
                )
                db.commit()
                return self.get_doc_by_name(name)
        except Exception as e:
            log.exception(e)
            return None

    def delete_doc_by_name(self, name: str) -> bool:
        try:
            with get_db() as db:

                db.query(Document).filter_by(name=name).delete()
                db.commit()
                return True
        except:
            return False

    def delete_doc_by_name_and_user(self, name: str, user_id: str) -> Optional[DocumentModel]:
        try:
            with get_db() as db:
                doc_to_be_deleted = db.query(Document).filter_by(name=name, user_id=user_id).first()
                db.query(Document).filter_by(name=name, user_id=user_id).delete()
                db.commit()
                return DocumentModel.model_validate(doc_to_be_deleted) if doc_to_be_deleted else None
                # return doc_to_be_deleted
        except:
            return False

Documents = DocumentsTable()
