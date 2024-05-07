from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from num2words import num2words

endpoint = ''
key = ''

def abstractive_summarization(text) -> str:
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

    poller = text_analytics_client.begin_abstract_summary(text)
    abstract_summary_results = poller.result()
    for result in abstract_summary_results:
        if result.kind == "AbstractiveSummarization":
            summary = [summary.text for summary in result.summaries]
        elif result.is_error is True:
            print("...Is an error with code '{}' and message '{}'".format(
                result.error.code, result.error.message
            ))
    return summary

def keywords_extraction(text)->list:
    text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    result = text_analytics_client.extract_key_phrases(text)
    keywords = []
    for doc in result:
        if not doc.is_error:
            keywords.append(doc.key_phrases)
    return keywords