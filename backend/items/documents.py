# from django_elasticsearch_dsl import Document, fields
# from elasticsearch_dsl import analyzer, tokenizer
# from django_elasticsearch_dsl.registries import registry
# from .models import Item

# autocomplete_analyzer = analyzer(
#     'autocomplete',
#     tokenizer=tokenizer(
#         'autocomplete_tokenizer',
#         'edge_ngram',
#         min_gram=1,
#         max_gram=20,
#         token_chars=['letter', 'digit'],
#     ),
#     filter=['lowercase'],
# )

# @registry.register_document
# class ItemDocument(Document):
#     name = fields.TextField(
#         analyzer=autocomplete_analyzer,
#         fields={
#             'raw': fields.KeywordField(),  
#         },
#     )
#     description = fields.TextField(analyzer=autocomplete_analyzer)
#     article = fields.TextField(analyzer=autocomplete_analyzer)

#     class Index:
#         name = 'items'
#         settings = {
#             'number_of_shards': 1,
#             'number_of_replicas': 1,
#             'analysis': {
#                 'analyzer': {
#                     'autocomplete': {
#                         'type': 'custom',
#                         'tokenizer': 'autocomplete_tokenizer',
#                         'filter': ['lowercase'],
#                     },
#                 },
#                 'tokenizer': {
#                     'autocomplete_tokenizer': {
#                         'type': 'edge_ngram',
#                         'min_gram': 1,
#                         'max_gram': 20,
#                         'token_chars': ['letter', 'digit'],
#                     },
#                 },
#             },
#         }

#     class Django:
#         model = Item
#         fields = []

from django_elasticsearch_dsl import Document, fields
from elasticsearch_dsl import analyzer, tokenizer
from django_elasticsearch_dsl.registries import registry
from .models import Item

autocomplete_analyzer = analyzer(
    'autocomplete',
    tokenizer=tokenizer(
        'autocomplete_tokenizer',
        'edge_ngram',
        min_gram=1,
        max_gram=20,
        token_chars=['letter', 'digit'],
    ),
    filter=['lowercase'],
)

@registry.register_document
class ItemDocument(Document):
    name = fields.TextField(
        analyzer=autocomplete_analyzer,
        fields={
            'raw': fields.KeywordField(),  # Для фильтрации и сортировки
            'standard': fields.TextField(analyzer='standard'),  # Для точного поиска
        },
    )
    description = fields.TextField(analyzer='standard')
    article = fields.TextField(analyzer='standard')
    category = fields.TextField(
        attr='category.name',  
        fields={'raw': fields.KeywordField()},
    )
    popularity = fields.IntegerField()  # если есть, для сортировки

    class Index:
        name = 'items'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 1,
            'analysis': {
                'analyzer': {
                    'autocomplete': {
                        'type': 'custom',
                        'tokenizer': 'autocomplete_tokenizer',
                        'filter': ['lowercase'],
                    },
                },
                'tokenizer': {
                    'autocomplete_tokenizer': {
                        'type': 'edge_ngram',
                        'min_gram': 1,
                        'max_gram': 20,
                        'token_chars': ['letter', 'digit'],
                    },
                },
            },
        }

    class Django:
        model = Item
        fields = []

