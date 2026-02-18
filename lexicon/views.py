from rest_framework.generics import ListAPIView
from .serializers import WordListSerializer
from .models import Word
class WordListView(ListAPIView):
    serializer_class = WordListSerializer

    def get_queryset(self,request):
        """
        Dynamically filter words base on the 'src' query parameter.
        
        """
        source_lang_code = self.request.query_params.get('src', 'de')
        
        return  Word.objects.select_related('language').filter(language__code = source_lang_code)