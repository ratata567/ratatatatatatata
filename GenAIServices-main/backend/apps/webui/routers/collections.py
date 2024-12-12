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
from constants import ERROR_MESSAGES

router = APIRouter()


@router.get("/", response_model=List[CollectionResponse])
async def get_collections(user=Depends(get_current_user)):
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

    # print("HERE #################")
    # print(Collections.get_collections_of_user(user.id))


    cols = [
        CollectionResponse(
            **{
                **col.model_dump(),
                "type" : "collection",
                "title" : col.collection_name,
                "name" : col.collection_name,
                "collection_names" : [col.collection_name]
            } 
        )
        for col in Collections.get_collections_of_user(user.id)
        # for doc in Documents.get_docs()
    ]
    # print(cols)
    return cols

@router.post("/create", response_model=Optional[bool])
async def delete_doc_by_name(collection_name: str, user=Depends(get_current_user)):
    col = Collections.insert_new_collection(user.id, collection_name)
    if col:
            # print("Here2")
            return True
    else:
        # print("Here3")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERROR_MESSAGES.FILE_EXISTS,
        )

############################
# DeleteDocByName
############################


@router.delete("/collection/delete", response_model=bool)
async def delete_doc_by_name(collection_name: str, user=Depends(get_current_user)):
    return_val = Collections.delete_collection_of_user(user.id, collection_name)
    # delete_docs_from_vector_db()
    return return_val
