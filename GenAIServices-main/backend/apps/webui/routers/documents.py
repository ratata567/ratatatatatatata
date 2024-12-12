from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from typing import List, Union, Optional

from fastapi import APIRouter
from pydantic import BaseModel
import json

from apps.webui.models.documents import (
    Documents,
    DocumentForm,
    DocumentUpdateForm,
    DocumentModel,
    DocumentResponse,
)
from apps.webui.models.collections import (
    Collections,
    CollectionResponse
)

from apps.rag.main import delete_docs_from_vector_db
from utils.utils import get_current_user, get_admin_user
from apps.rag.main import store_docs_in_vector_db, delete_docs_from_vector_db, get_loader
from constants import ERROR_MESSAGES
import mimetypes
from config import (
    UPLOAD_DIR,
);


router = APIRouter()

############################
# GetDocuments
############################


@router.get("/", response_model=List[DocumentResponse])
async def get_documents(user=Depends(get_current_user)):
    # doc = Documents.get_docs_of_user(user.id)
    # print("############")
    # if doc:
    # return DocumentResponse(
    #     **{
    #         **doc.model_dump(),
    #         "content": json.loads(doc.content if doc.content else "{}"),
    #     }
    # )
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail=ERROR_MESSAGES.NOT_FOUND,
    #     )

    docs = [
        DocumentResponse(
            **{
                **doc.model_dump(),
                "content": json.loads(doc.content if doc.content else "{}"),
            }
        )
        for doc in Documents.get_docs_of_user(user.id)
        # for doc in Documents.get_docs()
    ]
    # print(docs)
    return docs

# @router.get("/collections", response_model=List[CollectionResponse])
# async def get_collections(user=Depends(get_current_user)):
#     # doc = Documents.get_docs_of_user(user.id)

#     # if doc:
#     # return DocumentResponse(
#     #     **{
#     #         **doc.model_dump(),
#     #         "content": json.loads(doc.content if doc.content else "{}"),
#     #     }
#     # )
#     # else:
#     #     raise HTTPException(
#     #         status_code=status.HTTP_401_UNAUTHORIZED,
#     #         detail=ERROR_MESSAGES.NOT_FOUND,
#     #     )

#     # print("HERE #################")
#     # print(Collections.get_collections_of_user(user.id))


#     cols = [
#         CollectionResponse(
#             **{
#                 **col.model_dump(),
#                 "type" : "collection",
#                 "title" : col.collection_name,
#                 "name" : col.collection_name,
#                 "collection_names" : [col.collection_name]
#             } 
#         )
#         for col in Collections.get_collections_of_user(user.id)
#         # for doc in Documents.get_docs()
#     ]
#     # print(cols)
#     return cols


############################
# CreateNewDoc
############################


@router.post("/create", response_model=Optional[DocumentResponse])
async def create_new_doc(form_data: DocumentForm, user=Depends(get_current_user)):
    # doc = Documents.get_doc_by_name(form_data.name)
    # print("1111111111111111111")

    # print(form_data)
    doc = Documents.get_doc_by_name_and_user(form_data.name,user.id)
    # print(**doc.model_dump())
    # print("Hereeeeee")
    # print(doc)
    # print(form_data.vector_ids)
    # print("777777777777777777")
    print(Collections.insert_new_collection(user.id, form_data.collection_name))
    if doc == None:
        doc = Documents.insert_new_doc(user.id, form_data)
        # print(doc)
        # print("Here1")
        if doc:
            # print("Here2")
            return DocumentResponse(
                **{
                    **doc.model_dump(),
                    "content": json.loads(doc.content if doc.content else "{}"),
                }
            )
        else:
            # print("Here3")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERROR_MESSAGES.FILE_EXISTS,
            )
    else:
        # print("Here4")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.NAME_TAG_TAKEN,
        )


############################
# GetDocByName
############################


@router.get("/docs", response_model=Optional[DocumentResponse])
async def get_doc_by_name(name: str, user=Depends(get_current_user)):
    doc = Documents.get_doc_by_name(name)

    if doc:
        return DocumentResponse(
            **{
                **doc.model_dump(),
                "content": json.loads(doc.content if doc.content else "{}"),
            }
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# TagDocByName
############################


class TagItem(BaseModel):
    name: str


class TagDocumentForm(BaseModel):
    name: str
    tags: List[dict]


@router.post("/doc/tags", response_model=Optional[DocumentResponse])
async def tag_doc_by_name(form_data: TagDocumentForm, user=Depends(get_current_user)):
    doc = Documents.update_doc_content_by_name_and_user(form_data.name,user.id, {"tags": form_data.tags})

    if doc:
        return DocumentResponse(
            **{
                **doc.model_dump(),
                "content": json.loads(doc.content if doc.content else "{}"),
            }
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ERROR_MESSAGES.NOT_FOUND,
        )


############################
# UpdateDocByName
############################


@router.post("/doc/update", response_model=Optional[DocumentResponse])
async def update_doc_by_name(
    name: str, form_data: DocumentUpdateForm, user=Depends(get_current_user)
):
    # doc = Documents.update_doc_by_name(name, form_data)
    # print("Here1")
    doc_to_be_updated = Documents.get_doc_by_name_and_user(name, user.id)
    # print("Here2")
    old_collection = doc_to_be_updated.collection_name
    vector_ids = doc_to_be_updated.vector_ids
    if form_data.collection_name != old_collection:
        filename =  doc_to_be_updated.filename

        file_path = f"{UPLOAD_DIR}/{filename}"

        mime_type, encoding = mimetypes.guess_type(file_path)


        f = open(file_path, "rb")
        f.close()

        loader, known_type = get_loader(filename, mime_type, file_path)
        data = loader.load()

        result = store_docs_in_vector_db(data, form_data.collection_name)

        delete_docs_from_vector_db(old_collection, vector_ids)
        vector_ids = ""
        for id in result:
            vector_ids = vector_ids + id + ","

        vector_ids = vector_ids[0:-1]
    # print("Here3")
    form_data.vector_ids = vector_ids
    # print(form_data)
    doc = Documents.update_doc_by_name_and_user(name, user.id, form_data)
    if doc:
        return DocumentResponse(
            **{
                **doc.model_dump(),
                "content": json.loads(doc.content if doc.content else "{}"),
            }
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.NAME_TAG_TAKEN,
        )


############################
# DeleteDocByName
############################


@router.delete("/doc/delete", response_model=Optional[DocumentResponse])
async def delete_doc_by_name(name: str, user=Depends(get_current_user)):
    doc_to_be_deleted = Documents.delete_doc_by_name_and_user(name, user.id)
    # delete_docs_from_vector_db()
    return DocumentResponse(
            **{
                **doc_to_be_deleted.model_dump(),
                "content": json.loads(doc_to_be_deleted.content if doc_to_be_deleted.content else "{}"),
            }
        )
