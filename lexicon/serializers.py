from rest_framework import serializers
from .models import Word,Example,Definition,Category,Book,Lesson,Translation


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields=['id','title','level']

class LessonSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    class Meta:
        model = Lesson
        fields = ['id','book','lesson']
class TranslationSerializer(serializers.ModelSerializer):
    language_code = serializers.CharField(source='language.code',read_only=True)

    class Meta:
        model = Translation
        fields=['id','language_code','text']

class ExampleSerializer(serializers.ModelSerializer):
    translation = TranslationSerializer(many=True,read_only=True)
    native_language = serializers.CharField(source='language.code',read_only=True)
    class Meta:
        model = Example
        fields = ['id','text','translation','audio_url']


class DefinitionSerializer(serializers.ModelSerializer):
    translation = TranslationSerializer(source='translation.text')
    linked_examples = ExampleSerializer(many=True,read_only=True)
    language_code = serializers.CharField(source='language.code',read_only=True)

    class Meta:
        model = Definition
        fields = ['id','language_code','text','linked_examples','translation']

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id','name','slug','description']

class WordSerializer(serializers.ModelSerializer):
    definitions = DefinitionSerializer(source='definition', many=True, read_only=True)
    language_code = serializers.CharField(source='language.code', read_only=True)
    lesson = LessonSerializer(source='concept.lesson',many=True, read_only=True)
    category = CategorySerializer(source='concept.category',read_only=True)
    class Meta:
        model = Word
        fields = [
            'id', 'text', 'pos', 'cefr_level', 'audio_url', 
            'language_code', 'metadata', 'category', 'lesson', 'definitions'
        ]



class WordListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Word
        fields = ['id','text','pos','language_code']
