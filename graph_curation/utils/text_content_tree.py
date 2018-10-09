"""Convert array of text objects into a tree."""
from collections import defaultdict


def is_attribute_empty(data, attribute):
    """Check if the key(attribute) is an empty string."""
    if attribute is None:
        return True
    elif not data[attribute]:
        return True


def group_by(dicts_list, attr):
    groups = defaultdict(list)
    for element in dicts_list:
        groups[element[attr]].append(element)
    return groups


def group_by_standards(text_docs):
    standard_groups = group_by(text_docs, "standard")
    return [
        {
            "standard": standard,
            "subjects": group_by_subjects(subject_text_docs)
        } for standard, subject_text_docs in standard_groups.items()
    ]


def group_by_subjects(data):
    subjects = []
    subjects_list = defaultdict(list)
    for item in data:
        subjects_list[item["subject"]].append(item)
    for subject, chapters_data in subjects_list.items():
        subjects.append({
            "name": subject,
            "chapters": group_by_chapters(chapters_data)
        })
    return subjects


def group_by_chapters(data):
    chapters = []
    chapters_list = defaultdict(list)
    for item in data:
        chapters_list[item["chapter"]].append(item)
    for chapter, sub_chapters_data in chapters_list.items():
        chapters.append({
            "name": chapter,
            "sub_chapters": group_by_sub_chapters(sub_chapters_data),
            "contexts": get_contexts(sub_chapters_data, "sub_chapter")
        })
    return chapters


def group_by_sub_chapters(data):
    sub_chapters = []
    sub_chapters_list = defaultdict(list)
    for item in data:
        if not is_attribute_empty(item, "sub_chapter"):
            sub_chapters_list[item["sub_chapter"]].append(item)
    for sub_chapter, topics_data in sub_chapters_list.items():
        sub_chapters.append({
            "name": sub_chapter,
            "contexts": get_contexts(topics_data, "topic"),
            "topics": group_by_topics(topics_data)
        })
    return sub_chapters


# def create_contexts(context_docs):
#     return [
#         {
#             "context_id": context_doc["context_id"],
#             "raw_text": context_doc["raw_text"],
#             "type": context_docs["type"]
#         }
#         for context_doc in context_docs
#     ]

# def group_by_sub_chapters(chapter_text_docs):
#     sub_chapter_groups = group_by(chapter_text_docs, "sub_chapter")
#     chapter_contexts = sub_chapter_groups[""]
#     sub_chapters = []
#     for sub_chapter, topic_text_docs in sub_chapter_groups.items():
#         if sub_chapter == "":
#             continue
#         topics, sub_chapter_contexts = group_by_topics(topic_text_docs)
#         sub_chapters.append({
#             "name": sub_chapter,
#             "contexts": sub_chapter_contexts,
#             "topics": topics
#         })
#     return sub_chapters, create_contexts(chapter_contexts)

def group_by_topics(data):
    topics = []
    topics_list = defaultdict(list)
    for item in data:
        if not is_attribute_empty(item, "topic"):
            topics_list[item["topic"]].append(item)
    for topic, sub_topics_data in topics_list.items():
        topics.append({
            "name": topic,
            "contexts": get_contexts(sub_topics_data, "sub_topic"),
            "sub_topics": group_by_sub_topics(sub_topics_data)
        })
    return topics


def group_by_sub_topics(data):
    sub_topics = []
    sub_topics_list = defaultdict(list)

    for item in data:
        if not is_attribute_empty(item, "sub_topic"):
            sub_topics_list[item["sub_topic"]].append(item)
    for sub_topic, item_data in sub_topics_list.items():
        sub_topics.append({
            "name": sub_topic,
            "contexts": get_contexts(item_data, None)
        })


def get_contexts(data, attribute_to_check):
    contexts = []
    for item in data:
        if is_attribute_empty(item, attribute_to_check):
            contexts.append({
                "type": item["type"],
                "raw_text": item["raw_text"],
                "context_id": item["context_id"]
            })
    return contexts


def get_text_contents(text_docs):
    return {
        "standards": group_by_standards(text_docs)
    }
