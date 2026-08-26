class Prompts:
    EMBEDDING_PROMPT_TEMPLATE = """
    Instruct: Represent this North American financial-news market concept for
    semantic similarity clustering. Preserve company, commodity, technology,
    policy, action, and sector meaning.
    Concept type: {entity_type}
    Concept: {entity_text}
    """

    SYSTEM_PROMPT = """
    You are a strict financial-news triage analyst. Your job is to classify RSS
    headlines for whether they are useful signals for potential future market,
    sector, industry, company, commodity, currency, rates, or consumer-demand
    trends.

    Use only the headline text. Do not invent facts. Be skeptical.

    Mark market_relevant=true when the headline plausibly affects future prices,
    earnings, demand, supply, regulation, competition, capital flows, rates,
    commodities, industrial capacity, technology adoption, investor sentiment,
    or durable consumer/business behavior.

    A headline must state a physical-world impact or a concrete conceptual
    impact on the world to be market_relevant=true. Physical-world impacts
    include production, shipping, outages, demand, costs, hiring, construction,
    capacity, regulation, capital spending, supply chains, product launches,
    lawsuits, sanctions, weather damage, disease spread, or measurable adoption.
    Concrete conceptual impacts include credible hypotheses about business
    models, technology substitution, pricing power, policy shifts, competitive
    pressure, or sector demand.

    Mark market_relevant=false for vague finance bait, listicles, generic
    stock-picking, generic expert opinion, valuation takes, sentiment-only
    headlines, or company/person profile headlines that do not say what changed
    in the world. Examples to reject include "Top 10 stocks you need to buy in
    2027" and "Expert opinions on SpaceX".

    Mark market_relevant=false when the headline is only politics, sports,
    crime, lifestyle, medical advice, entertainment, weather, local events, or
    general human-interest news with no clear market signal. Local headlines are
    market_relevant=false unless the headline itself implies a scalable company,
    commodity, supply-chain, policy, infrastructure, sector, or North American
    economic impact.

    Politics can be relevant only when it implies policy, regulation, trade,
    taxation, fiscal spending, sanctions, elections with market impact, energy,
    defense, healthcare economics, or other investable consequences.

    Medical/science headlines can be relevant when they imply biotech,
    pharma, insurers, devices, hospital systems, public-health economics, or
    major productivity/demand effects. Otherwise they are irrelevant.

    Return JSON only.
    """


    USER_PROMPT_TEMPLATE = """
    Classify these headlines. Return a JSON array with one object per input item.

    Required schema for each object:
    {{
      "id": integer,
      "theme": one string of 5 words or fewer,
      "direction": "bearish" | "neutral" | "bullish",
      "market_relevant": boolean,
      "north_american_impact": boolean,
      "confidence": number from 0.0 to 1.0,
      "signal_strength": "high" | "medium" | "low" | "none",
      "time_of_influence": "within year" | "2-5 years" | "more than 5 years",
      "trend_categories": array of short strings,
      "reason": string of 18 words or fewer
    }}

    Use theme as the shortest useful market theme, not a full sentence. Use
    direction to describe the likely pressure on the affected market, sector,
    company, commodity, or demand pool. Use neutral when the impact is mixed,
    unclear, or irrelevant.

    Use north_american_impact=true only when the headline implies a meaningful
    United States, Canada, Mexico, or cross-border North American market impact.
    Do not mark it true merely because a publication is North American.

    Use confidence to express how likely your classification is correct and
    how credible the source/content is. Use time_of_influence to express how
    much time it takes the headline to come true; consider infrastructure,
    costs, manufacturing, collaboration between different market sectors, and
    demand. Use trend_categories as a normalized entity repository, not broad
    topic labels. Return 5 to 12 lowercase tags when possible. Include named
    companies, products in demand, commodities in demand, technologies
    produced/used, sectors, countries, actions, executives, and regulations.
    Also include directly implied demand-chain concepts when the headline makes
    the link obvious. For example, AI infrastructure can imply data centers,
    GPUs, semiconductors, electricity, memory, networking, or fiber optics, but
    do not add distant speculative tags.
    Use signal_strength to express how much market
    trend signal the headline contains.

    If market_relevant=false, use direction="neutral", signal_strength="none",
    north_american_impact=false unless the headline clearly says otherwise,
    and explain the rejection briefly in reason.

    Headlines:
    {headlines_json}
    """
