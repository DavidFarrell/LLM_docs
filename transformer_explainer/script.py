"""Narration script for the Transformer explainer.

Each scene is a list of (beat_key, text) pairs. `{name}` marks a bookmark:
the time at which the *next* word starts is exported so animations can be
synced to it. `[word](/phonemes/)` overrides pronunciation (misaki syntax).
"""

SCRIPT = {
    # ------------------------------------------------------------------ 01
    "S01_ColdOpen": [
        ("b1", "Here's a sentence. {w0}The {w1}animal {w2}didn't {w3}cross {w4}the {w5}street "
               "{w6}because {w7}it {w8}was {w9}too {w10}tired."),
        ("b2", "You knew instantly that {it}'it' means the animal. "
               "But swap one word, {wide}tired for wide, and {now}'it' becomes the street."),
        ("b3", "To get this right, a model has to let each word {look}look at the other words "
               "and decide which of them matter. In {year}twenty seventeen, a team at Google "
               "published an architecture built around exactly that idea, and very little else. "
               "The paper's title says it all: {title}Attention Is All You Need."),
        ("b4", "That architecture, {transformer}the Transformer, is {gpt}the T in GPT, and it sits "
               "at the heart of {llm}nearly every large language model today."),
        ("b5", "We're going to rebuild it from scratch, with two goals. {one}First, to make queries, "
               "keys and values feel obvious, including why they're called that. {two}And second, "
               "to see exactly how attention plugs into the rest of the neural network."),
    ],
    # ------------------------------------------------------------------ 02
    "S02_Recurrence": [
        ("b1", "First, what did it replace? The leading translation systems of the time were "
               "mostly {rnn}recurrent neural networks. They read a sentence {one}one word at a time, "
               "carrying a running summary, {hidden}called a hidden state, from each step to the next."),
        ("b2", "That creates two problems. {dist}The first is distance. For information about "
               "'animal' to reach 'it', {pass}it has to survive being passed through every step in "
               "between. {far}The further apart two words are, the harder their relationship is to learn."),
        ("b3", "{speed}The second is speed. Step fifty can't begin until step forty-nine has "
               "finished, {gpu}so the work can't be spread across the thousands of cores in a GPU."),
        ("b4", "The Transformer's answer was radical. {drop}Drop recurrence entirely, and "
               "{all}let every word look directly at every other word, all at once. "
               "{onestep}Any two words are now a single step apart, "
               "{par}and the whole sentence can be processed in parallel."),
    ],
    # ------------------------------------------------------------------ 03
    "S03_Vectors": [
        ("b1", "To see how one word 'looks at' another, we need to see what the model sees. "
               "Each word, or more precisely each sub-word token, {vec}becomes a list of numbers: "
               "a vector. {dim}In the paper, each one has five hundred and twelve dimensions."),
        ("b2", "You can think of these as {space}coordinates in a space of meaning, "
               "{rel}where related words point in related directions."),
        ("b3", "And the tool for comparing two vectors is {dot}the dot product: "
               "{mult}multiply matching entries and add them up. {same}Similar directions give a "
               "large positive score, {perp}unrelated ones give roughly zero, {opp}and opposite "
               "ones go negative. {built}Everything that follows is built on this one operation."),
    ],
    # ------------------------------------------------------------------ 04
    "S04_Lookup": [
        ("b1", "Now, the nouns. {qkv}Query, key and value come from a very ordinary idea: "
               "{lookup}looking something up."),
        ("b2", "Picture {dict}a dictionary in code. It stores pairs. {key}Each pair has a key, "
               "the label you search by, {val}and a value, the thing you get back. "
               "{q}Ask for 'France'. That request is {query}the query. {cmp}The system compares it "
               "against each key, {match}finds the match, {ret}and returns the value: Paris."),
        ("b3", "Notice that the key and the value are different things. {k}'France' is how the "
               "entry is found. {v}'Paris' is what the entry gives you. {sep}That separation is "
               "why there are three nouns, not two."),
        ("b4", "A normal lookup is all or nothing: one exact match, one value back. "
               "{soft}Attention makes it soft. {score}Instead of demanding a match, it scores how "
               "well the query fits every key, {w}turns the scores into weights that add up to one, "
               "{blend}and returns a blend of all the values, mixed by those weights."),
        ("b5", "That is, almost word for word, how the paper defines it. {quote}An attention "
               "function maps a query and a set of key-value pairs to an output: {ws}a weighted "
               "sum of the values, {compat}with each weight set by how compatible the query is "
               "with the corresponding key."),
        ("b6", "Why soft? {diff}Because a soft lookup is differentiable. {nudge}Nudge the query "
               "and the weights shift smoothly, {learn}so gradient descent can learn what to look "
               "for. {hard}A hard lookup would give it nothing to learn from."),
    ],
    # ------------------------------------------------------------------ 05
    "S05_SelfAttention": [
        ("b1", "In a Transformer, the thing being looked up is {sent}the sentence itself, and "
               "every word plays all three roles. {q}Each word sends out a query: what am I "
               "looking for? {k}Each offers a key: what do I contain? {v}And each holds a value: "
               "what will I pass on if someone attends to me?"),
        ("b2", "Take {it}'it'. Loosely speaking, its query asks: which noun do I refer to? "
               "{ak}The key of 'animal' advertises something like: singular noun, a creature, "
               "something that can get tired. {av}And the value of 'animal' carries what's worth "
               "passing on: the meaning of 'animal' itself."),
        ("b3", "But those descriptions are cartoons. {nobody}Nobody writes them. "
               "{mat}Queries, keys and values are produced by three weight matrices that the "
               "model learns: {wq}W Q, {wk}W K and {wv}W V. {mul}Multiply a word's vector by "
               "each, and out come its query, its key and its value."),
        ("b4", "Now the lookup. {dot}The query of 'it' is dotted with the key of every word in "
               "the sentence, {scores}giving one score per word. {high}A high score means that "
               "key is a good answer to that query."),
        ("b5", "{soft}Softmax turns the scores into weights: all positive, summing to one. "
               "{most}Here, most of the weight lands on 'animal'."),
        ("b6", "{scale}Then each word's value is scaled by its weight, {sum}and the results are "
               "added up. {new}The output is a new vector for 'it', one that now carries "
               "information from 'animal'. {ctx}The word has absorbed its context."),
        ("b7", "{all}And every word does this at the same time, each with its own query. "
               "{sa}That's self-attention."),
    ],
    # ------------------------------------------------------------------ 06
    "S06_WhyThree": [
        ("b1", "So why bother with three versions of each word? {direct}Why not just compare the "
               "word vectors directly?"),
        ("b2", "Try it, and two things go wrong. {self}First, every word tends to be most similar "
               "to itself, so each would mostly attend to itself. {sym}Second, a dot product is "
               "symmetric: 'it' would care about 'animal' exactly as much as 'animal' cares about "
               "'it'. {asym}But relevance is one-directional. The pronoun badly needs the noun; "
               "the noun barely needs the pronoun."),
        ("b3", "Separate query and key matrices fix both. {fix}The score from one word to another "
               "becomes a learned, one-way question: does what I'm looking for match what you're "
               "offering? {val}And a separate value matrix means what a word advertises can "
               "differ from what it actually hands over."),
        ("b4", "So: {q}the query is what I'm looking for. {k}The key is what I can be found by. "
               "{v}The value is what I give when I'm found. {names}The names come straight from "
               "a database lookup, made soft, and made learnable."),
    ],
    # ------------------------------------------------------------------ 07
    "S07_Matrix": [
        ("b1", "In practice, none of this happens one word at a time. {stack}Stack every word's "
               "query as a row of a matrix, Q. {kv}Do the same for the keys, K, and the values, V."),
        ("b2", "{qk}Then Q times K transpose computes every query against every key in a single "
               "matrix multiplication: {grid}a grid of scores, {rows}one row for each word doing "
               "the asking, {cols}one column for each word being asked."),
        ("b3", "{div}Divide by the square root of d k, the key dimension. {sm}Apply softmax along "
               "each row, so each word's attention adds up to one. {v}Then multiply by V, "
               "{out}and each row of the result is a context-aware version of its word."),
        ("b4", "{eq}Put together, that's equation one in the paper, which it calls scaled dot-product attention. "
               "{every}Every symbol in it is something you've just seen built."),
        ("b5", "That square root is doing real work. {var}If the entries of a query and a key "
               "are random, with variance one, their dot product has variance d k. {sd}With "
               "sixty-four dimensions, typical scores are around plus or minus eight."),
        ("b6", "{sat}Softmax on numbers that large saturates. Nearly all the weight piles onto "
               "one word, {grad}and the gradients become tiny, so learning slows to a crawl. "
               "{fix}Dividing by the square root of d k brings the scores back to a sensible range."),
    ],
    # ------------------------------------------------------------------ 08
    "S08_MultiHead": [
        ("b1", "One attention pattern can only capture one kind of relationship at a time. "
               "But words relate in many ways at once: {ex1}what a pronoun refers to, "
               "{ex2}which word came just before, {ex3}which verb goes with which subject."),
        ("b2", "{heads}So the Transformer runs several attentions in parallel, called heads. "
               "{own}Each head has its own W Q, W K and W V, so each learns to ask a different "
               "kind of question. {eight}The paper uses eight heads, each working in sixty-four "
               "dimensions."),
        ("b3", "{cat}Their outputs are concatenated back to five hundred and twelve dimensions, "
               "{wo}and mixed by one more learned matrix, W O. {cost}Because each head is "
               "smaller, eight of them cost about the same as one full-sized head."),
        ("b4", "And heads really do specialise. {fig}In the paper's appendix, heads in layer five "
               "link the word {its}'its' straight back to {law}'Law', the noun it refers to. "
               "{just}Just like 'it' and 'animal' in our example."),
    ],
    # ------------------------------------------------------------------ 09
    "S09_Position": [
        ("b1", "There's a catch hiding in all this. {order}Attention has no idea about word "
               "order. {shuf}Shuffle the input, and every word gets exactly the same output as "
               "before, just in a new slot. {dog}To attention alone, 'dog bites man' and "
               "'man bites dog' look the same."),
        ("b2", "The fix is to stamp each position onto its word. {add}Before the first layer, a "
               "positional encoding is added to every word's embedding. {waves}The paper builds "
               "it from sine and cosine waves of different frequencies: {fast}fast in some "
               "dimensions, {slow}slow in others, like the hands of a clock, {sig}so every "
               "position gets a unique signature."),
        ("b3", "{lin}And because of how sines and cosines work, moving a fixed number of "
               "positions along is a simple linear transformation, {rel}which the authors "
               "hoped would make relative positions easy to learn."),
    ],
    # ------------------------------------------------------------------ 10
    "S10_EncoderLayer": [
        ("b1", "Now for the second big question. {how}How does attention actually fit into the "
               "neural network? {build}Let's build one encoder layer."),
        ("b2", "{lanes}Picture each word's vector travelling upward in its own lane. "
               "{attn}First comes multi-head attention, where the lanes talk to each other, "
               "{gather}and every word gathers information from the rest."),
        ("b3", "{res}The attention output doesn't replace the word's vector. {added}It's added "
               "onto it. This is a residual connection. {doc}Think of each vector as a running "
               "document. Each layer doesn't rewrite it; {upd}it writes an update, and the "
               "update is added in."),
        ("b4", "{norm}Then layer normalisation re-centres and rescales each vector, keeping its "
               "numbers in a stable range, which helps training. {formula}The paper writes this "
               "as layer norm of x, plus sublayer of x. {an}Add and norm."),
        ("b5", "{ffn}Next comes the part that's easy to overlook: a feed-forward network. "
               "{classic}It's a classic neural network with one hidden layer. {up}It takes each "
               "word's five hundred and twelve numbers, expands them to two thousand and "
               "forty-eight, {relu}applies a [ReLU](/ɹˈAlu/), which zeroes the negatives, "
               "{down}and projects back down to five hundred and twelve."),
        ("b6", "{same}Crucially, the same network is applied to each position separately. "
               "{nomove}No information moves between words here. {div}So there's a division of "
               "labour. {comm}Attention is communication: words exchange information. "
               "{comp}The feed-forward network is computation: each word processes what it "
               "has gathered."),
        ("b7", "It's not a minor part, either. {params}The feed-forward network holds about two "
               "thirds of each encoder layer's parameters. {mem}And later research suggests it "
               "works like a memory: {fk}its first layer detects patterns, like keys, "
               "{fv}and its second writes out a value for each pattern it finds. "
               "{again}The same idea again, frozen into weights."),
        ("b8", "{add2}One more add and norm, and that's a complete encoder layer. "
               "{stack}The encoder stacks six of them. {deep}Each layer's attention works on "
               "vectors that earlier layers have already enriched with context, so later layers "
               "can capture subtler relationships."),
        ("b9", "{learn}And every matrix in the stack, every W Q, W K and W V, W O, and both "
               "feed-forward layers, {bp}is learned together by backpropagation, from a single "
               "training signal: {sig}how well the model predicts each next word of the correct "
               "translation. {nobody}No one tells the heads what to ask. {emerge}The questions emerge."),
    ],
    # ------------------------------------------------------------------ 11
    "S11_Decoder": [
        ("b1", "The paper's task was translation: {en}English to German. {enc}The encoder turns "
               "the English sentence into a set of context-rich vectors. {dec}The decoder then "
               "writes the German, one token at a time."),
        ("b2", "Each decoder layer has three parts. {mask}First, masked self-attention: each "
               "position may only attend to itself and the words before it, never to future "
               "ones. {inf}The scores for future positions are set to minus infinity before the "
               "softmax, {zero}so their weights come out as exactly zero."),
        ("b3", "{cross}The second part is where the nouns really earn their names: "
               "encoder-decoder attention. {dq}The queries come from the decoder: I'm about to "
               "write the next German word, so what in the English matters? {ek}The keys and "
               "values come from the encoder's output. {ans}The decoder asks; the English answers."),
        ("b4", "{ffn}The third part is the same feed-forward network, {an}with add and norm "
               "around every part, {six}and again, six layers."),
        ("b5", "{lin}At the top, a linear layer and a softmax turn the final vector into "
               "probabilities over the whole vocabulary, {vocab}about thirty-seven thousand "
               "tokens. {pick}The model picks a likely next token, {app}appends it, and goes again."),
        ("b6", "{train}In training, though, the full target sentence is already known, "
               "{mask2}so with the mask in place, every position can be predicted at once. "
               "{fast}That's a big part of why Transformers train so much faster than "
               "recurrent networks."),
        ("b7", "{fig}And here's the full diagram from the paper. {every}Every box on it is "
               "something you've now seen built."),
    ],
    # ------------------------------------------------------------------ 12
    "S12_Legacy": [
        ("b1", "The results were striking. {bleu}On English-to-German translation, the big "
               "Transformer scored twenty-eight point four blue, {two}more than two points above "
               "the best previous systems, including ensembles. {days}And it trained in three "
               "and a half days on eight GPUs, a fraction of the cost of the models it beat."),
        ("b2", "{later}Within a year or two, the same blocks were everywhere. {bert}Bert kept "
               "the encoder stack. {gpt}GPT kept the decoder stack. {scale}Scale that up, train "
               "it on vast amounts of text, and you get today's language models. {core}The "
               "details have been refined, but the core loop is still this paper's: "
               "{attend}attend, {compute}compute, {repeat}repeat."),
    ],
    # ------------------------------------------------------------------ 13
    "S13_Recap": [
        ("b1", "So, one last time. {q}Every word asks a question: its query. {k}Every word "
               "advertises what it contains: its key. {v}And every word offers something to "
               "share: its value. {attn}Attention matches questions to keys, and blends the "
               "matching values into each word."),
        ("b2", "{ffn}Then the feed-forward network lets each word process what it gathered, "
               "{res}residual connections keep the running record, {stack}and the stack repeats, "
               "layer after layer, until every word's vector reflects the whole sentence."),
        ("b3", "{end}That's the Transformer. Attention wasn't quite all you need, "
               "{but}but it was the idea that changed everything."),
    ],
}


def iter_beats():
    for scene, beats in SCRIPT.items():
        for key, text in beats:
            yield scene, key, text


if __name__ == "__main__":
    import re
    total = 0
    for scene, beats in SCRIPT.items():
        n = sum(len(re.sub(r"\{\w+\}|\(/[^)]*/\)", "", t).split()) for _, t in beats)
        total += n
        print(f"{scene:22s} {n:5d} words")
    print("TOTAL", total, "words  ~", round(total / 160, 1), "min at 160 wpm")
