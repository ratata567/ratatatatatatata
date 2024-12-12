from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from typing import List, Union, Optional

from fastapi import APIRouter
from pydantic import BaseModel
import json

from apps.webui.models.documents import (
<<<<<<<< HEAD:backend/apps/web/temp/routers/documents.py
    Documents,
    DocumentForm,
    DocumentUpdateForm,
    DocumentModel,
    DocumentResponse,
)

from apps.webui.models.collections import (
========
>>>>>>>> d3146d20ad74c020855142b2bf7e371f981ec098:backend/apps/webui/routers/documents.py
    Documents,
    DocumentForm,
    DocumentUpdateForm,
    DocumentModel,
    DocumentResponse,
)

from utils.utils import get_verified_user, get_admin_user
from constants import ERROR_MESSAGES

router = APIRouter()

############################
# GetDocuments
############################


@router.get("/", response_model=List[DocumentResponse])
<<<<<<<< HEAD:backend/apps/web/temp/routers/documents.py
async def get_documents(user=Depends(get_current_user)):
    # doc = Documents.get_docs_of_user(user.id)

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

========
async def get_documents(user=Depends(get_verified_user)):
>>>>>>>> d3146d20ad74c020855142b2bf7e371f981ec098:backend/apps/webui/routers/documents.py
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
    return docs


############################
# CreateNewDoc
############################


@router.post("/create", response_model=Optional[DocumentResponse])
async def create_new_doc(form_data: DocumentForm, user=Depends(get_current_user)):
    # doc = Documents.get_doc_by_name(form_data.name)
    doc = Documents.get_doc_by_name_and_user(form_data.name,user.id)
    # print(**doc.model_dump())
    # print(doc)
    Collections
    if doc == None:
        doc = Documents.insert_new_doc(user.id, form_data)
        # print(doc)
        # print("Here1")
        if doc:
            print("Here2")
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


@router.get("/doc", response_model=Optional[DocumentResponse])
async def get_doc_by_name(name: str, user=Depends(get_verified_user)):
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


<<<<<<<< HEAD:backend/apps/web/temp/routers/documents.py
@router.post("/name/{name}/tags", response_model=Optional[DocumentResponse])
async def tag_doc_by_name(form_data: TagDocumentForm, user=Depends(get_current_user)):
    doc = Documents.update_doc_content_by_name_and_user(form_data.name,user.id, {"tags": form_data.tags})
========
@router.post("/doc/tags", response_model=Optional[DocumentResponse])
async def tag_doc_by_name(form_data: TagDocumentForm, user=Depends(get_verified_user)):
    doc = Documents.update_doc_content_by_name(form_data.name, {"tags": form_data.tags})
>>>>>>>> d3146d20ad74c020855142b2bf7e371f981ec098:backend/apps/webui/routers/documents.py

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
<<<<<<<< HEAD:backend/apps/web/temp/routers/documents.py
    name: str, form_data: DocumentUpdateForm, user=Depends(get_current_user)
========
    name: str,
    form_data: DocumentUpdateForm,
    user=Depends(get_admin_user),
>>>>>>>> d3146d20ad74c020855142b2bf7e371f981ec098:backend/apps/webui/routers/documents.py
):
    # doc = Documents.update_doc_by_name(name, form_data)
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


<<<<<<<< HEAD:backend/apps/web/temp/routers/documents.py
@router.delete("/name/{name}/delete", response_model=bool)
async def delete_doc_by_name(name: str, user=Depends(get_current_user)):
    result = Documents.delete_doc_by_name_and_user(name, user.id)
========
@router.delete("/doc/delete", response_model=bool)
async def delete_doc_by_name(name: str, user=Depends(get_admin_user)):
    result = Documents.delete_doc_by_name(name)
>>>>>>>> d3146d20ad74c020855142b2bf7e371f981ec098:backend/apps/webui/routers/documents.py
    return result
