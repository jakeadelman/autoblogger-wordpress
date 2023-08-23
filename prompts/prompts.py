SUMMARIZE_PROMPT = """Write a detailed summary that captures all relevant information of the following text.
The summary should be at least 500 words.
If there is anything about asking to prove you are human, don't write about it in the summary response.
Make it in the style of a blog writer who is talking about the subject rather than from the point of view of a company that owns the product.
Don't add any additional text that isn't found in the text to summarize.
Don't make anything up. Don't have any cut-off sentences.
Don't include anything that is not specifically on the topic of "{topic}"

Text to summarize: "{text}"

DETAILED SUMMARY:"""

