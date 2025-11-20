"""
Utils for integrating NLP parser with Django database
"""
from typing import Dict, List
from .synonyms import SYNONYMS

# cache for combined synonyms
_cached_synonyms = None


def extract_course_field_from_name(course_name: str) -> str:
    """
    Takes a course name and gets the main subject from it by removing qualifications and common words.

    :param course_name: Full course name including qualifications (e.g., "Computer Science BSc (Hons)")
    :return: Cleaned course name as lowercase string (e.g., "computer science")
    """
    if not course_name:
        return ""
    # endif
    
    clean = course_name.lower()
    
    # remove common qualifications and brackets
    removals = [
        ' (hons)', ' hons', ' bsc', ' ba', ' msc', ' ma',
        ' meng', ' msci', ' llb', ' bds', ' mbbs',
        ' degree', ' programme', ' program', ' course',
        ' - ', ' with ', ' and ', ' & ', '(', ')'
    ]
    
    for r in removals:
        clean = clean.replace(r, ' ')

    #endfor
    
    # remove extra spaces
    clean = ' '.join(clean.split())
    
    return clean.strip()
# enddef


def load_combined_synonyms() -> Dict:
    """
    Gets all the subjects and course names from the database and combines them
    with the hardcoded synonym list for parsing.

    :return: Dictionary containing subjects, courses, dropped phrases, interest phrases, and none phrases
    """
    global _cached_synonyms
    
    # start with hardcoded synonyms
    combined = {
        "subjects": SYNONYMS["subjects"].copy(),
        "courses": SYNONYMS["courses"].copy(),
        "dropped": SYNONYMS["dropped"],
        "interest": SYNONYMS["interest"],
        "none": SYNONYMS["none"]
    }
    
    try:
        # only try to load from database if Django is properly set up
        import django
        from django.apps import apps
        
        if apps.ready:
            # import models here to avoid circular imports
            from mysite.apps.coursefinder.models import Course, SubjectRequirement
            
            # get unique course names from database
            course_names = Course.objects.values_list('name', flat=True).distinct()
            
            for name in course_names:
                if not name:
                    continue
                # endif
                
                # use our function to clean the course name
                clean_name = extract_course_field_from_name(name)
                
                # add to courses dict if not already there
                if clean_name and clean_name not in combined["courses"]:
                    # create a new entry with the course name mapping to itself
                    combined["courses"][clean_name] = [clean_name, name.lower()]
                elif clean_name and clean_name in combined["courses"]:
                    # add as an alias if not already there
                    if name.lower() not in combined["courses"][clean_name]:
                        combined["courses"][clean_name].append(name.lower())
                    # endif
                # endif
            # endfor
            
            # get unique subjects from subject requirements
            subject_names = SubjectRequirement.objects.values_list('subject', flat=True).distinct()
            
            for name in subject_names:
                if not name:
                    continue
                # endif
                    
                clean_name = name.lower().strip()
                
                # add to subjects dict if not already there
                if clean_name and clean_name not in combined["subjects"]:
                    combined["subjects"][clean_name] = [clean_name]
                # endif
            # endfor
        # endif
        
    except Exception as e:
        # just use hardcoded if database not available
        pass
    # endtry
    
    # cache the result
    _cached_synonyms = combined
    return combined
# enddef


def get_synonyms() -> Dict:
    """
    Gets the cached combined synonyms dictionary.

    :return: Dictionary containing all synonym data (subjects, courses, dropped, interest, none)
    """
    global _cached_synonyms
    
    if _cached_synonyms is None:
        load_combined_synonyms()
    # endif
    
    return _cached_synonyms
# enddef