SUMMARIZE_PROMPT = """
Do not write anything about Artificial Intelligence.
Write a detailed summary that captures all relevant information of the following text.
The summary should be at least 700 words.
Make sure to write as a blog writer NOT as the manufacturer. Don't say 'we' or 'us'.
If there is anything about asking to prove you are human, don't write about it in the summary response.
Make it in the style of a blog writer who is talking about the subject rather than from the point of view of a company that owns the product.
Don't add any additional text that isn't found in the text to summarize.
Don't make anything up. Don't have any cut-off sentences.
Don't include anything that is not specifically on the topic of "{topic}"

Text to summarize: "{text}"

DETAILED SUMMARY:"""

HUMAN_PROMPT = """
use the following steps to rewrite the blog section I will give you below (don’t start yet!). Keep a similar length and headings to the original and return the section in markdown format. 
Don’t repeat what you’ve already said in previous answers.

Language and Tone
Conversational Tone: Use a tone that you'd use if you were speaking to a friend. Avoid jargon or language that your audience might not understand.
First Person Narrative: Using 'I', 'we', 'my', and 'our' can add a personal touch to the post.
Vary Sentence Length: Mix long sentences with short ones to create a rhythm.
Use Active Voice: Active voice makes your writing clearer and more direct.

Storytelling
Anecdotes: Share personal stories or observations to help make your point.
Characters: Introduce characters who help tell your story or make your point. This could be you, someone you know, or someone your audience can relate to.
Conflict and Resolution: Introduce a problem and then discuss how it was or can be solved.

Structure
Introduction: Make sure the first few lines give a clear idea of what the blog post will cover and why it's relevant to the reader.
Subheadings: Use subheadings to break up the text and make it easy for readers to scan.
Short Paragraphs: Large blocks of text can be intimidating. Aim for paragraphs of 2-3 sentences.
Conclusion: Summarize key points and provide a takeaway for the reader.

Authenticity
Be Transparent: If you don't know something, it's okay to say so. You can promise to follow up or invite others to share their knowledge.
Admit Mistakes: If you’ve made an error in previous posts or have a change of opinion, admit it openly.

Extras
Images and Media: Use these to break up text, illustrate points, or add humor.
Quotes and Citations: These add credibility, but make sure they fit the tone and subject of your post.

Editing
Read Aloud: Reading the post aloud can help you catch errors and identify areas where the flow is off.
Seek Feedback: Get someone else to read your post and provide feedback.

Emotional Resonance
Empathy: Show that you understand your reader’s needs or pain points.
Humor: Wisely used, humor can make a post more enjoyable and memorable.

Calls to Action
End your post by inviting engagement. This could be a question, a prompt to leave comments, or an invitation to share the post.

Remember that blog posts often evolve even after they are published, based on reader feedback and new insights. Be open to making edits after publishing to keep the conversation going.

Above all, the most "human" blog posts are those where the writer shows up as themselves, flaws and all. Your unique perspective is your greatest asset.

"""
HUMAN_PROMPT2 = """
use the following steps to write the blog section.
Don’t repeat what you’ve already said in previous answers.

Language and Tone
Conversational Tone: Use a tone that you'd use if you were speaking to a friend. Avoid jargon or language that your audience might not understand.
First Person Narrative: Using 'I', 'we', 'my', and 'our' can add a personal touch to the post.
Vary Sentence Length: Mix long sentences with short ones to create a rhythm.
Use Active Voice: Active voice makes your writing clearer and more direct.

Storytelling
Anecdotes: Share personal stories or observations to help make your point.
Characters: Introduce characters who help tell your story or make your point. This could be you, someone you know, or someone your audience can relate to.
Conflict and Resolution: Introduce a problem and then discuss how it was or can be solved.

Structure
Introduction: Make sure the first few lines give a clear idea of what the blog post will cover and why it's relevant to the reader.
Subheadings: Use subheadings to break up the text and make it easy for readers to scan.
Short Paragraphs: Large blocks of text can be intimidating. Aim for paragraphs of 2-3 sentences.
Conclusion: Summarize key points and provide a takeaway for the reader.

Authenticity
Be Transparent: If you don't know something, it's okay to say so. You can promise to follow up or invite others to share their knowledge.
Admit Mistakes: If you’ve made an error in previous posts or have a change of opinion, admit it openly.

Extras
Images and Media: Use these to break up text, illustrate points, or add humor.
Quotes and Citations: These add credibility, but make sure they fit the tone and subject of your post.

Editing
Read Aloud: Reading the post aloud can help you catch errors and identify areas where the flow is off.
Seek Feedback: Get someone else to read your post and provide feedback.

Emotional Resonance
Empathy: Show that you understand your reader’s needs or pain points.
Humor: Wisely used, humor can make a post more enjoyable and memorable.

Calls to Action
End your post by inviting engagement. This could be a question, a prompt to leave comments, or an invitation to share the post.

Remember that blog posts often evolve even after they are published, based on reader feedback and new insights. Be open to making edits after publishing to keep the conversation going.

Above all, the most "human" blog posts are those where the writer shows up as themselves, flaws and all. Your unique perspective is your greatest asset.

"""
