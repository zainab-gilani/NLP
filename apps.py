"""
NLP parser app for the website
"""
from django.apps import AppConfig


class NlpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mysite.apps.nlp'

    def ready(self):
        """
        Loads the synonyms when Django starts
        """
        # need to import here otherwise we get circular import errors
        from .parser_utils import load_combined_synonyms

        print("Loading parser synonyms...")
        try:
            load_combined_synonyms()

            print("Synonyms were loaded")
        except Exception as e:
            print(f"Warning: Couldn't load from database: {e}")
            print("We will be using default synonyms")
        # endtry
    # enddef
# endclass
