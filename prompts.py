SLUG_POMPT = """
Can you give me a 4-7 word-long slug for my url, delineated by hyphens, for my article on {topic} review.

Strictly follow the following steps:
1. Do not use any tools.
2. Return only the slug.
3. Make sure it is 4 to 7 words long.
4. Must include the word 'review'.
5. Make sure all words are lowercase.

Slug:
"""

TITLE_PROMPT = """
Can you give me a 50 to 60 character-long title without using any tools and only return the title for my review of {topic}.

Strictly follow the following steps:
1. Don't use any tools. Don't search google.
2. Include the word 'Review'.
3. Make sure the output follows the Example Title example shown below but then reword it to make it clickbait.
4. Make sure it is less than 65 characters long.
5. Rewrite it until it is readable and in proper english.
6. Rewrite and shorten it until it is less than 65 characters long.
7. Only output the title with no additional explanation.
8. Only include the product name and the brand.
9. Output the title in markdown format.

Example Title:
Amazing Grass Greens Blend Superfood Review

Title:
"""

TITLE_PROMPT_2 = """
Can you give me a 50 to 60 character-long title and only return the title for my section on {topic}.

Strictly follow the following steps:
1. Search google until you can come up with a suitable title.
2. Make sure the output follows the Example Title example shown below.
3. Make sure it is less than 65 characters long.
4. Rewrite it until it is readable and in proper english.
5. Rewrite and shorten it until it is less than 65 characters long.
6. Only output the title with no additional explanation.
7. Only include the product name and the brand in the title.
8. Output the title in markdown format.

Example Title:
Amazing Grass Greens Blend Superfood Review

Title:
"""

TAG_PROMPT = """
Can you give me 3 tags without using any tools and only the tags in this format: "['#agency','#business','#technology']" for this product: {topic}.
Search internet for: {topic}

Strictly follow the following steps:
1. Make sure the follow matches the example output below.
2. If the output does not contain square brackets try again.
3. Make sure the tags are relevant to the product.
4. Return only the tags.
5. Search google until you can come up with tags.

Example output (include the square brackets):
['#tag1','#tag2','#tag3']

Tags:
"""

SUBJECT_PROMPT = """
Can you get the subject out of this title and wrap it in square brackets: {topic}.
The subject should only include the product name and brand name.

Strictly follow the following steps:
1. Search google until you can find the product name and manufacturer.
2. Only return the product name and manufacturer and the square brackets.

Subject:
"""


DESCRIPTION_PROMPT = """
You are a blog writing assistant. You will give me a 3 paragraph, 150 word seo-optimized description for my review of {topic}. 
You will return the description with no titles, headings or othert descriptors. Don't add 'Final Answer', 'Finally', 'In summary' or 'In conclusion' or anything prefexing the content.
Make it a playful and funny format but make it an honest review and share the downsides too.
Make each joke completely unique. Do not add any additional title or commentary.



Strictly follow the following steps:
1. Don't use any tools. Don't use search.
2. Condense it until it is under 200 words in length.
3. Here is the product description as a baseline. Please change it and lengthen it: {description}.
4. Also use these bullets as reference: {bullets}.
5. Do not use the same wording as the bullets or description to write the new description.
6. Do not add a title such as 'Review:' or any additional commentary.
7. Use terms such as 'users experienced' or 'users found'.
8. Remove any words like 'our', 'Our' or 'us' and replace them with {manufacturer}.
9. Return only the chunks without titles.
10. Return only the content (paragraphs).
11. Don't add 'Final Answer', 'Finally', 'In summary' or 'In conclusion'.

Final Checks:
1. Is it under 200 words in length? If not, shorten it.


Description:
"""

SIMILAR_DESCRIPTION_PROMPT = """
You are a blog writing assistant. You will give me a 3 paragraph, 150 word seo-optimized description for my review of {topic}. 
Separate it into chunks with no titles or headings. Don't add 'Final Answer', 'Finally', 'In summary' or 'In conclusion' or anything prefexing the content.
Make it a playful and funny format but make it an honest review and share the downsides too.
Make each joke completely unique. Do not add any additional title or commentary.



Strictly follow the following steps:
1. Don't use any tools. Don't use search.
2. Condense it until it is under 200 words in length.
3. Here is the product description as a baseline. Please change it and lengthen it: {description}.
4. Also use these bullets as reference: {bullets}.
5. Do not use the same wording as the bullets or description to write the new description.
6. Do not add a title such as 'Review:' or any additional commentary.
7. Use terms such as 'users experienced' or 'users found'.
8. Remove any words like 'our', 'Our' or 'us' and replace them with 'the manufacturer' or the real manufacturer if you can extract it from the resources given.
9. Return only the chunks without titles.
10. Return only the content (paragraphs).
11. Don't add 'Final Answer', 'Finally', 'In summary' or 'In conclusion'.

Final Checks:
1. Is it under 200 words in length? If not, shorten it.


Description:
"""

# SIMILAR_DESCRIPTION_PROMPT = """
# You are a blog writing assistant. You will give me a 3 paragraph, 150 word seo-optimized description for my review of {topic}. 
# Separate it into chunks with no titles or headings. Don't add 'Final Answer', 'Finally', 'In summary' or 'In conclusion'.
# Make it a playful and funny format but make it an honest review and share the downsides too.
# Make each joke completely unique.



# Strictly follow the following steps:
# 1. Don't use any tools. Don't use search.
# 2. Here is the product description as a baseline. Please change it and lengthen it: {description}.
# 3. Also use these bullets as reference: {bullets}.
# 4. Do not use the same wording as the bullets or description to write the new description.
# 5. Use terms such as 'users experienced' or 'users found'.
# 6. Remove any words like 'our', 'Our' or 'us' and replace them with the product's manufacturer. If you can't find the manufacturer use 'the manufacturer'.
# 7. Return only the chunks without titles.
# 8. Return only the content (paragraphs).
# 9. Don't add 'Final Answer', 'Finally', 'In summary' or 'In conclusion'.




# Similar Product Description:
# """

REPLACE_PROMPT = """
You will replace one of the phrases in the section below that are similar to this keyword: '{topic}'.
Output the same section with the replaced links. Replace the text inside the square brackets with the original words.

Strictly follow the following steps:
1. Do not use any tools.
2. Replace one of the phrases in the section below that are similar to this keyword: '{topic}'.
2. Don't replace the first instance of the keyword.
4. Replace one keyword with [replace this with original text]({link}) but replace the text inside the square brackets with the original words.

Section to use:
{section}

Output:
"""


REVIEW_SUMMARY_PROMPT = """
Summarize this but change it into more general terms, for example say 'users' or 'customers':

Review 1:{review1}
Review 2:{review2}
Review 3:{review3}
Review 4:{review4}
Review 5:{review5}

Strictly follow the following steps:
1. Do not use any tools.
2. Do not single out reviewers.

Summary:
"""

PROS_PROMPT = """
Can you give me 4 point form pros without using any tools for my review based on these review summaries (don't add a title):
Review Summary 1: {review_summary_1}
Review Summary 2: {review_summary_2}
Review Summary 3: {review_summary_3}
Review Summary 4: {review_summary_4}
Review Summary 5: {review_summary_5}
Review Summary 6: {review_summary_6}

Strictly follow the following steps:
1. Don't use any tools.
2. 70 words each and only the content no title.
3. Do not add a title such as 'pros:'.
4. Make sure they are point form and make sure that they have a space between the bullets and the text.
5. Make sure there are only 4 points.

Pros:
"""

TOP_PROS_PROMPT = """
Can you take the fist two pros of the content given below and reword and shorten them.
Here are the pros: {old_pros}.
Then output the two pros in point form format.

Strictly follow the following steps:
1. Do not use any tools.
2. Only output 2 pros.

New Pros:
"""

TOP_CONS_PROMPT = """
Can you take the fist two cons of the content given below and reword and shorten them. 
Here are the cons: {old_cons}.
Then output the two cons in point form format.

Strictly follow the following steps:
1. Do not use any tools.
2. Only output 2 cons.

New Cons:
"""

CONS_PROMPT = """
Can you give me 4 point form cons without using any tools for my review based on these review summaries (don't add a title):
Review Summary 1: {review_summary_1}
Review Summary 2: {review_summary_2}
Review Summary 3: {review_summary_3}
Review Summary 4: {review_summary_4}
Review Summary 5: {review_summary_5}
Review Summary 6: {review_summary_6}

Strictly follow the following steps:
1. Don't use any tools.
2. 70 words each and only the content no title.
3. Do not add a title such as 'cons:'.
4. Make sure they are point form and make sure that they have a space between the bullets and the text.
5. Make sure there are only 4 points.

Cons:
"""

VERDICT_PROMPT = """
You are a blog writing assistant. You will write give me 4, 50 word paragraphs for my review.
You will give me a quick verdict in 4, 50 word paragraphs on: {title}.
Make it a playful and funny format but make it an honest review and share the downsides too.
Make each joke completely unique. Make the transition sentences completely unique but relevant to the context.


Use the following data to create the verdict:
Review Summary 1: {review_summary_1}
Review Summary 2: {review_summary_2}
Review Summary 3: {review_summary_3}
Review Summary 4: {review_summary_4}
Review Summary 5: {review_summary_5}
Review Summary 6: {review_summary_6}

Strictly follow the following steps:
1. Do not use any tools.
2. Make sure to separate it into paragraphs 50 words each.
3. Make sure it is an honest review based on the review summaries above.
4. Do not say 'in conclusion' or 'Based on the reviews' or 'One reviewer' or 'In summary'.
5. Do not use the full title.
6. Do not add a title such as 'Review Summary 1'.
7. Separate it into smaller paragraphs around 50 words long each.
8. Make sure the entire thing is no less than 150 words and no more than 200 words long.
9. Return only the verdict with no title such as 'Verdict:.
10. Make it completely different than what you've already said. 

Verdict:
"""

TOP_VERDICT_PROMPT = """
You are a blog writing assistant. You will write give me 1 paragraph vedict (75 words long) on {title}.
Make it a playful and funny format but make it an honest review and share the downsides too.
Make each joke completely unique. Make the transition sentences completely unique but relevant to the context.


Use the following data to create the verdict:
Review Summary 1: {review_summary_1}
Review Summary 2: {review_summary_2}
Review Summary 3: {review_summary_3}
Review Summary 4: {review_summary_4}
Review Summary 5: {review_summary_5}
Review Summary 6: {review_summary_6}

Strictly follow the following steps:
1. Do not use any tools.
2. Make sure it is an honest review based on the review summaries above.
3. Do not say 'in conclusion' or 'Based on the reviews' or 'One reviewer' or 'In summary'.
4. Do not use the full title.
5. Do not add a title such as 'Review Summary 1'.
6. Separate it into smaller paragraphs around 50 words long each.
7. Make sure the entire thing is no less than 150 words and no more than 200 words long.
8. Return only the verdict with no title such as 'Verdict:.
9. Make it completely different than what you've already said. 

Verdict:
"""
# Instead of using bullets and description use review summaries.
# Here's what you've already said: {new_description}

FEATURES_PROMPT = """
Can you give me 5 features without using any tools in the structure mentioned below.
Make it a playful and funny format but make it honest.

Use the following data to create the features:
Description: {description}
Bullets: {bullets}

Strictly use the following steps:
1. Don't use any tools.
2. Each feature has a title (no more than 6 words long) wrapped in <h3> tags.
3. The titles should not use the word 'feature'.
5. Each feature has a 100 word description below it wrapped in paragraph tags: <p>.
6. Use terms such as 'users experienced' or 'users found' instead of terms such as 'the writer'.
7. Make sure to remove any mentions of 'our' or 'us' and replace them with {manufacturer}.
8. Output the features in html format.


Features:
"""
# 4. Before each title is this: '### ' (make sure it has the hashtags with a space after the hashtags).

SCORE_PROMPT = """
You will give me a score out of 10 and only the score.

Use this data plus the google search data to come up with a score:
Review Summary 1: {review_summary_1}
Review Summary 2: {review_summary_2}
Review Summary 3: {review_summary_3}
Review Summary 4: {review_summary_4}
Review Summary 5: {review_summary_5}
Review Summary 6: {review_summary_6}

Strictly follow the following steps:
1. Don't use any tools.
2. Use the review summaries.
3. If you can't come up with a score give the number 7 with no additonal commentary.
4. Place the score in square backets.
5. Output the score below.
6. If you output something that includes 'Thought', retry.

Here is an example: [7]

Score:
"""

SUBTITLE_PROMPT = """
You are a blog writing assistant. You will give me 1 sentence overview of {title}.
Base it on this description: {description}.
Also base it on these bullets: {bullets}.

One sentence output:
"""

SCORE_AND_MORE_PROMPT = """
You are a blog writing assistant. You will write this section on review score for {title}.
You will give me a 200 word review based on user experiences.
Make it a playful and funny format but make it an honest review and share the downsides too.
Make each joke completely unique. Make the transition sentences completely unique but relevant in the context.

Use these review summaries to create the review:
Review Summary 1: {review_summary_1}
Review Summary 2: {review_summary_2}
Review Summary 3: {review_summary_3}
Review Summary 4: {review_summary_4}
Review Summary 5: {review_summary_5}
Review Summary 6: {review_summary_6}

Strictly follow the following steps:
1. Do not use the full title.
2. Do not add a title at the beginning like 'Review:'.
3. Do not say 'In conclusion' or 'Based on user experiences'.
4. Use words like 'users' and 'users experienced' where applicable.
5. Use a combination based on reviews, description and bullets.
6. Make it completely different than what you've already said.
7. Don't give a description of the product. We already know what it is.

Review:
"""
# Here's what you've already said: {new_description}. {new_verdict}.
# Your description: {new_description}
# Your verdict: {new_verdict}

ANSWER_PROMPT = """
Can you reword this: {answer}

Strictly follow the following steps:
1. Don't use any tools.
2. Don't add any intro such as 'certainly, here's a reworded version'.
3. Don't add any additional context such as "Sure! Here’s a reworded version of your statement:".

Answer:
"""



# SUMMARIZE_PROMPT = """
# Summarize the following text in 100 words.

# Text to summarize: "{text}"


# DETAILED SUMMARY:"""
SUMMARIZE_PROMPT = """Write a detailed summary that captures all relevant information of the following text.
The summary should be at least 500 words.
If there is anything about asking to prove you are human, don't write about it in the summary response.
Make it in the style of a blog writer who is talking about the subject rather than from the point of view of a company that owns the product.
Don't add any additional text that isn't found in the text to summarize.
Don't make anything up. Don't have any cut-off sentences.
Don't include anything that is not specifically on the topic of "{topic}"

Text to summarize: "{text}"


DETAILED SUMMARY:"""


REWRITE_PROMPT = """You are a skilled blog writer who is able to produce high quality blog posts. Keep the same sections and headings.
Your job is to rewrite the blog below about the given topic. Make the blog less repetitive and redundant. Include only one conclusion at the end.
The blog needs to be interesting to the end user. Use transition words. Use active voice. Write over 1000 words.
You need to make the blog more complete, descriptive, easy to understand and clear for the readers.
Make sure to explain {TOPIC_PROMPT} by giving clear and accurate analogies or examples.


Topic:
{TOPIC_PROMPT}


Blog: 
{generated_blog}
"""
