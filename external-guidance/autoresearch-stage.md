# The Lossfunk Autoresearch Challenge

In the near future, human researchers' cognitive labor will be in direct competition with AI systems. In the past, the justification of spending time researching an area was that someone else could use what you discover. But, now, if an AI system could do a similar job in a week for $100, what justifies a human spending months researching the same question?

The exercise in this stage is a forcing function: only by running an autoresearch system on your actual question can you find out whether spending months on it as a human is justified, or whether the question itself needs to change.

We'd rather you discover this in a week than six months in.

## What this is

The Autoresearch stage of the Lossfunk internship application. If you've made it past first stage (research proposal accepted against our rubric), this is the next step.

It's also a tool you can use even if you're not applying. The challenge is designed so that anyone who attempts it seriously will learn something true and important about what current auto-research systems can and cannot do — and about whether the kind of research they want to spend their career on is the kind Claude Code can already produce.

We think a lot of aspiring researchers are training for a job that won't exist in three years. If that's you, better to discover it now from a one-week exercise than five years into a PhD.

## What's expected of you

Take your research proposal that you submitted and spend seven days producing a first-draft research artifact using any AI auto-research system you choose. We personally use [Autovoila](https://github.com/paraschopra/autovoila), but you're welcome to use any system (they're just prompts). We will give a budget of $50 in credits/compute for this stage (initially $20, and if you require more, up to $30 more later).

Submit two things:

1. **The artifact itself.** Whatever your auto-research system produced — paper draft, experimental results, analysis, figures. Don't edit it. Upload on a github repo and submit what the AI produced.

2. **A presentation / deck** covering following topics:

    - Your **starting research question** / claim
    - Your **autoresearch flow**. What did you use? How did you go about it? Did you customize anything?
    - **Summary of results** found by AI (from autoresearch)
    - **What did you learn about your research question** from this sprint
    - **Critique of your own AI-generated artifact**. Specifically: what is genuinely correct and useful, what is plausible-looking mush, what is missing that you would have included, what is overclaimed, what would a senior researcher in this area immediately see as wrong. Be merciless. We are testing your taste, not your AI's output.
    - **Reflection on what you learned about the limits of current auto-research systems on this specific question**. What did the AI do well? Where did it fail? What kind of question would it have done better on? What does this tell you about which research questions are still worth a human's attention?
    - **Revised research plan** (if any): mention delta between original submitted one and revised one

That's the whole submission. No proposal revisions, no padding, no production value beyond what the AI produces. We are reading for judgment, not polish.

## Why this format

We're not testing whether you can do research. We're testing whether you can recognize what research is, separate it from what looks like research, and demonstrate that the recognition lives in you and not just in your tools.

The critique is the actual test. The artifact is the stimulus that lets us see your judgment in action.

If you've never had the experience of generating a confident-sounding research output and then sitting with it long enough to see what's actually wrong with it, you're missing the most important skill of the next decade. This exercise gives you that experience whether you get accepted or not.

## Best practices

- **Autovoila walkthrough**: Go these [slides](https://docs.google.com/presentation/d/1vYuz5glxBkTkqQgHIuIldrJYAe0j_2M0xTMxfJ2zRKU/edit) or [session](https://www.youtube.com/watch?v=ouQELzH5Zqc) to understand how autoresearch systems work
- **Use Frontier Models (like Claude Code / Codex)** In our experience, one end-to-end session with top model (Opus 4.7 xhigh as of May 2026) costs <$10. So you should be able to do a few iterations within the budget. If you're going over budget, you can cut the scope or use a cheaper model like Sonnet, but start with the top model to explore upper limits of today's AI systems.
- **Customize your setup.** You can modify the repo or build your own. Modify anything. Just tell us what you did.

What we want to see: real autonomous execution, not "I prompted ChatGPT five times and edited the output." If a human did the conceptual heavy lifting and the AI just smoothed the prose, that's not what we're testing. The point of the exercise is to see what happens when you actually try to push the limits of what current systems can do alone.

Be honest about the level of human intervention. Inflating AI autonomy makes your critique easier (because you're critiquing a partially-human artifact, which is naturally stronger) but it defeats the entire purpose of the exercise and we'll see through it.

## What we're looking for in the reflection

The reflection is graded on whether you've updated your model of what's worth working on, based on the evidence you just generated.

Some questions worth addressing (don't address all of them — pick what's actually relevant to what you learned):

- What is your auto-research system genuinely good at? Be precise.
- What is it bad at? Be precise.
- For your specific research question, did the AI produce something that a competent person could have produced themselves with a few weeks of work? If yes, this is a sign your question is in the redoable zone.
- What kind of question would have been harder for the AI? Why?
- Did your view of which research is worth doing change? In what direction?
- Are there questions you previously thought were interesting that you now think are essentially automated? What does that change about what you want to work on?

We are not looking for "AI is amazing" or "AI is useless." Both are wrong. We are looking for nuanced, specific observations about a real exercise you just ran.

## Anti-patterns

Things that will reduce your chance of being accepted:

- **Critiques that praise the artifact.** If your critique mostly says the AI did a good job, either you picked a question the AI is genuinely strong on (in which case your reflection should note this is a question Lossfunk shouldn't fund a human to do) or you're not seeing the failures (in which case your taste isn't ready).
- **Critiques that are uniformly damning without specifics.** "This is all garbage" is as useless as "this is great." Specificity is the signal.
- **Heavy editing of the artifact.** We want to see what the AI produced, not what you cleaned up. If the AI produced something embarrassingly bad, submit it embarrassingly bad and tell us what's wrong with it.
- **Borrowed critiques.** Don't run the artifact through Claude and ask Claude to critique it. We can tell. The critique should sound like a specific person with a specific view, not a balanced-perspectives essay. Idiosyncrasy and opinion are good; balanced caveats are bad.
- **Inflating autonomy.** Telling us the AI did everything when you actually intervened heavily. We'll ask follow-up questions and the inconsistencies will show.

## Logistics

- **Time budget:** 7 days from when you receive this challenge.
- **API costs:** Up to $50 in credits / compute. Lossfunk team will send you openrouter or cloud compute credits (initially $20, and if you require more, up to $30 more later).
- **Format:** Submit link to github repo and a deck (PDF)
- **Review timeline:** We aim to respond within 14 days of submission.

## Outcomes

After we review your submission, one of three things happens:

1. **Invitation to Stage 3** (a 30-minute live conversation). This means your critique demonstrated genuine taste and we want to talk to you. Roughly 1 in 5 submissions reach this point.

2. **Decline.** Most submissions stop here. We try to give one specific piece of feedback in the decline so the exercise has educational value beyond the outcome.

3. **Encouragement to redo with a different question.** Sometimes the question was the wrong vehicle to demonstrate taste — too far in either direction (too easy or too hard for current AI). If we think you'd succeed with a better-chosen question, we'll say so.

## Why we publish this

Two reasons.

First, transparency. We think research labs should be honest about what they're testing for. Hidden rubrics select for people who happen to think like the PI, which is a worse filter than the one we get from a public challenge that's hard to game.

Second, education. This exercise is valuable independent of whether you apply to Lossfunk. If you're a young researcher trying to figure out what to spend your career on, running this exercise honestly on a question you care about will teach you more in seven days than a year of incremental coursework. We'd rather a thousand people do this exercise than ten people apply to us.

If you do the exercise and don't apply, we'd be curious to hear what you learned. Even a paragraph emailed to us is useful — it helps us calibrate the challenge and write better versions of it over time.

## Final note

Take the exercise seriously. The version of you that emerges from one week of doing this honestly is more useful to the world than the version that submitted a polished proposal and waited.
