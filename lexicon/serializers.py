from rest_framework import serializers
from .models import Word,Example,Definition,Language


class ExampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Example
        fields = ['id','text','translation','audio_url']


class DefinitionSerializer(serializers.ModelSerializer):

    linked_examples = ExampleSerializer(many=True,read_only=True)
    language_code = serializers.CharField(source='language.code',read_only=True)

    class Meta:
        model:Definition
        fields = ['id','language_code','text','linked_examples']


class WordSerializer(serializers.ModelSerializer):
    definitions = DefinitionSerializer(many=True, read_only=True)
    language_code = serializers.CharField(source='language.code', read_only=True)
    class Meta:
        model = Word
        fields = ['id','text','pos','language_code','metadata','definitions']



class WordListSerializer(serializers.ModelSerializer):
    model = Word
    fields = ['id','text','pos','language_code']
