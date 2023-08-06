import pprint
import string
import uuid
from random import choices
from typing import List, TYPE_CHECKING, Union
from weakref import proxy

import sqlalchemy
from sqlalchemy import text

from ormar.fields.foreign_key import ForeignKeyField  # noqa I100

if TYPE_CHECKING:  # pragma no cover
    from ormar.models import FakePydantic, Model


def get_table_alias() -> str:
    return "".join(choices(string.ascii_uppercase, k=2)) + uuid.uuid4().hex[:4]


class RelationshipManager:
    def __init__(self) -> None:
        self._relations = dict()
        self._aliases = dict()

    @staticmethod
    def prefixed_columns(alias: str, table: sqlalchemy.Table) -> List[text]:
        return [
            text(f"{alias}_{table.name}.{column.name} as {alias}_{column.name}")
            for column in table.columns
        ]

    @staticmethod
    def prefixed_table_name(alias: str, name: str) -> text:
        return text(f"{name} {alias}_{name}")

    def add_relation_type(
        self,
        relations_key: str,
        reverse_key: str,
        field: ForeignKeyField,
        table_name: str,
    ) -> None:
        if relations_key not in self._relations:
            self._relations[relations_key] = {"type": "primary"}
            self._aliases[f"{table_name}_{field.to.Meta.tablename}"] = get_table_alias()
        if reverse_key not in self._relations:
            self._relations[reverse_key] = {"type": "reverse"}
            self._aliases[f"{field.to.Meta.tablename}_{table_name}"] = get_table_alias()

    def deregister(self, model: "FakePydantic") -> None:
        for rel_type in self._relations.keys():
            if model.get_name() in rel_type.lower():
                if model._orm_id in self._relations[rel_type]:
                    del self._relations[rel_type][model._orm_id]

    def add_relation(
        self,
        parent: "FakePydantic",
        child: "FakePydantic",
        child_model_name: str,
        virtual: bool = False,
    ) -> None:
        parent_id, child_id = parent._orm_id, child._orm_id
        parent_name = parent.get_name(title=True)
        child_name = (
            child_model_name
            if child.get_name() != child_model_name
            else child.get_name() + "s"
        )
        if virtual:
            child_name, parent_name = parent_name, child.get_name()
            child_id, parent_id = parent_id, child_id
            child, parent = parent, proxy(child)
            child_name = child_name.lower() + "s"
        else:
            child = proxy(child)

        parent_relation_name = parent_name.title() + "_" + child_name
        parents_list = self._relations[parent_relation_name].setdefault(parent_id, [])
        self.append_related_model(parents_list, child)

        child_relation_name = child.get_name(title=True) + "_" + parent_name.lower()
        children_list = self._relations[child_relation_name].setdefault(child_id, [])
        self.append_related_model(children_list, parent)

    @staticmethod
    def append_related_model(relations_list: List["Model"], model: "Model") -> None:
        for relation_child in relations_list:
            try:
                if relation_child.__same__(model):
                    return
            except ReferenceError:
                continue

        relations_list.append(model)

    def contains(self, relations_key: str, instance: "FakePydantic") -> bool:
        if relations_key in self._relations:
            return instance._orm_id in self._relations[relations_key]
        return False

    def get(
        self, relations_key: str, instance: "FakePydantic"
    ) -> Union["Model", List["Model"]]:
        if relations_key in self._relations:
            if instance._orm_id in self._relations[relations_key]:
                if self._relations[relations_key]["type"] == "primary":
                    return self._relations[relations_key][instance._orm_id][0]
                return self._relations[relations_key][instance._orm_id]

    def resolve_relation_join(self, from_table: str, to_table: str) -> str:
        return self._aliases.get(f"{from_table}_{to_table}", "")

    def __str__(self) -> str:  # pragma no cover
        return pprint.pformat(self._relations, indent=4, width=1)

    def __repr__(self) -> str:  # pragma no cover
        return self.__str__()
