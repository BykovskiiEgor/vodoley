import pytest


@pytest.fixture(autouse=True, scope="session")
def disable_elasticsearch_indexing():
    # Отключить сигналы документа
    from django_elasticsearch_dsl.registries import registry

    for doc in registry.get_documents():
        doc._doc_type.mapping = None
        doc._index = None
    registry._models = {}
