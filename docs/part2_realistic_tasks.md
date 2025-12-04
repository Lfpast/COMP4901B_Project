## Part 2 – Realistic Tasks and Agent Trajectories

This section demonstrates **three realistic tasks** that I would normally perform manually, and how they can instead be automated using my implemented `SearchAgent`.  
For each task, I:

- **Describe the real-world manual workflow**
- **Show a complete agent trajectory** with at least 5 steps and at least 3 different tools
- **Discuss whether the agent completed the task correctly**, and analyze what went wrong if not

All trajectories are based on the actual capabilities exposed in `tools.py`:  
**Valid tools (excluding search and browsing):** `google_shopping`, `google_maps_search`, `google_scholar`  
**Auxiliary tools:** `google_search`, `browse_website` (used to support main tools but don't count toward the 3-tool requirement)

---

## Task 1 – Preparing for an AI Conference Attendance

### 1.1 Real-World Manual Workflow

When I need to attend an academic conference (e.g., NeurIPS or CVPR) in Hong Kong, I would typically:

- Search Google Scholar for recent papers related to the conference topics to understand current research trends.
- Read abstracts and introductions of highly-cited papers to prepare questions for sessions.
- Use Google Maps to find hotels or Airbnbs near the conference venue, filtering by rating and price.
- Check accommodation websites for amenities (WiFi, workspace, distance to venue).
- Shop for conference essentials: professional voice recorder for sessions, portable charger, business card holder, and a quality notebook.
- Compare prices across different e-commerce platforms and check seller ratings.

### 1.2 Agent Configuration and Tools Used

To automate this with my agent, I configure:

- `SearchAgent(use_tools=True, use_browsing=True, use_shopping=True, enable_maps=True, enable_scholar=True)`

The main tools used in this trajectory:

- `google_scholar` – to discover relevant papers and understand conference themes.
- `google_maps_search` – to find suitable accommodation near the venue.
- `google_shopping` – to purchase conference equipment and supplies.
- `google_search` & `browse_website` – auxiliary tools for additional research.

### 1.3 Agent Trajectory (≥ 5 Steps, ≥ 3 Tools)

**Step 1 – Initial Reasoning (no tool)**  
The user asks: *"I'm attending an AI conference on multimodal learning in Kowloon next month. Help me: (1) find 3-5 important recent papers to read beforehand, (2) recommend a hotel within 15 minutes walk from the venue, and (3) suggest equipment I should buy, budget around HK$1000."*

The agent's internal reasoning identifies:
- Conference topic: *multimodal learning, AI*
- Location constraint: *Kowloon, Hong Kong*
- Tasks: *literature preparation + accommodation + shopping for equipment*

The agent decides to start with **Google Scholar** to understand the field.

**Step 2 – Scholar Search (`google_scholar`)**  
  The agent issues a tool call:
- Function: `google_scholar`
- Arguments:
  - `query = "multimodal learning vision language"`
  - `num = 15`
  - `year_low = 2022`

The tool returns a `papers` list containing:
- `title`, `authors`, `year`, `cited_by`, `pdf_link`, `snippet`

From the results, the agent identifies 5 highly-cited papers (e.g., CLIP variants, BLIP, Flamingo) with citation counts > 200 and published after 2022. These are recorded in `reasoning_steps`.

**Step 3 – Abstract Reading (`browse_website`)**  
For the top 3 papers, the agent:
- Extracts the `pdf_link` or arXiv link from the Scholar results.
- Calls `browse_website` with those URLs to read abstracts and introduction sections.
- Summarizes the key contributions: *"BLIP-2 introduces Q-Former for efficient vision-language alignment..."*

**Step 4 – Accommodation Search (`google_maps_search`)**  
The agent calls:
  - Function: `google_maps_search`
- Arguments:
  - `query = "hotel"`
  - `location = "Kowloon, Hong Kong"`
  - `num = 15`

Returns a list of hotels with `rating`, `reviews`, `price_level`, `address`, and `google_maps_link`. The agent filters for:
- Rating > 4.0
- Reviews > 100 (reliability indicator)
- Located within reasonable distance to common conference venues

**Step 5 – Hotel Website Verification (`browse_website`)**  
For 2-3 promising hotels, the agent:
- Calls `browse_website` on their `website` URLs.
- Checks for amenities: *"free WiFi", "workspace", "breakfast included", "conference room nearby"*
- Verifies distance to common conference centers via the Maps link.

**Step 6 – Shopping for Conference Equipment (`google_shopping`)**  
The agent calls:
- Function: `google_shopping`
  - Arguments:  
  - Multiple queries in sequence:
    - `query = "voice recorder conference Hong Kong"`
    - `query = "portable charger 20000mAh Hong Kong"`
    - `query = "business card holder professional"`
  - `num = 10` for each

Returns shopping results with `title`, `price`, `source`, `rating`. The agent filters for:
- Total budget ≤ HK$1000
- Good seller ratings
- Suitable specifications (e.g., recorder with >8 hours battery)

**Step 7 – Price Comparison (`google_search`)**  
For specific products identified in shopping, the agent:
- Issues `google_search` queries like: *"Sony ICD-PX470 review Hong Kong best price"*
- Checks snippets for user reviews and potential better deals.

**Step 8 – Final Recommendation (no further tools)**  
The agent produces a final answer:
- **Papers**: Lists 5 papers with 2-3 sentence summaries and suggested reading order (foundational → recent).
- **Hotel**: Recommends 1-2 hotels with addresses, ratings, and booking links.
- **Equipment**: Lists specific products with prices, purchase links, and total cost breakdown.

### 1.4 Correctness and Failure Analysis

**Overall outcome:**  
The agent successfully completes this multi-faceted task:
- `google_scholar` ensures academically relevant paper recommendations.
- `google_maps_search` provides reliable accommodation options with ratings.
- `google_shopping` delivers budget-appropriate equipment suggestions.

**Potential failure modes:**
- Some arXiv PDFs may have complex LaTeX rendering that `browse_website` cannot parse cleanly, potentially missing key details in abstracts.
- Hotel pricing in Maps data may be outdated or unavailable; the agent must then rely on website browsing which may fail for JavaScript-heavy booking sites.
- Shopping results can be time-sensitive; prices fluctuate and stock availability is not guaranteed.
- The agent might over-prioritize citation count for papers, potentially missing very recent (but impactful) work with few citations yet.

Despite these limitations, the agent dramatically reduces manual effort compared to separately searching Scholar, Maps, and shopping platforms by hand.

---

## Task 2 – Course Project Preparation: Few-Shot Learning Research

### 2.1 Real-World Manual Workflow

When starting a machine learning course project on few-shot learning, I would:

- Search Google Scholar for foundational and recent papers on few-shot learning.
- Read paper abstracts to identify key methods (meta-learning, prototypical networks, etc.).
- Find a quiet study location with good WiFi—using Google Maps to search for libraries, study cafes, or co-working spaces.
- Visit cafe websites or Maps reviews to check: noise level, power outlets, seating comfort, time limits.
- Purchase study materials and equipment: ML textbooks, external hard drive for datasets, second monitor for coding.
- Compare prices and read reviews on e-commerce sites.

### 2.2 Agent Configuration and Tools Used

To automate this with my agent, I configure:

- `SearchAgent(use_tools=True, use_browsing=True, use_shopping=True, enable_maps=True, enable_scholar=True)`

The main tools used:

- `google_scholar` – to find relevant papers on few-shot learning.
- `google_maps_search` – to find suitable study locations (libraries, cafes).
- `google_shopping` – to purchase study materials and hardware.
- `google_search` & `browse_website` – auxiliary tools for additional information.

### 2.3 Agent Trajectory (≥ 5 Steps, ≥ 3 Tools)

**Step 1 – Initial Reasoning (no tool)**  
The user asks: *"I'm starting a course project on few-shot learning. Please: (1) recommend 5 important papers to read, (2) find 2-3 quiet study places in Tsim Sha Tsui with WiFi, and (3) suggest study equipment to buy with a budget of HK$3000."*

The agent identifies:
- Research topic: *few-shot learning*
- Location: *Tsim Sha Tsui, Hong Kong*
- Budget: *HK$3000 for equipment*

**Step 2 – Literature Search (`google_scholar`)**  
The agent calls:
- Function: `google_scholar`
- Arguments:
  - `query = "few-shot learning meta-learning"`
  - `num = 20`
  - `year_low = 2019`

Returns papers including classic works (Matching Networks, Prototypical Networks) and recent advances. The agent selects 5 papers balancing:
- Foundational methods (high citations)
- Recent innovations (2022-2024)
- Diverse approaches (meta-learning, metric learning, data augmentation)

**Step 3 – Paper Abstract Extraction (`browse_website`)**  
For each of the 5 selected papers:
- Calls `browse_website` on `pdf_link` (usually arXiv).
- Extracts abstract and first paragraphs of introduction.
- Summarizes: *"Prototypical Networks learn a metric space where classification is performed by computing distances to prototype representations..."*

**Step 4 – Study Location Search (`google_maps_search`)**  
  The agent calls:
- Function: `google_maps_search`
- Arguments:
  - `query = "library study cafe quiet"`
  - `location = "Tsim Sha Tsui, Hong Kong"`
  - `num = 15`

Returns places with `rating`, `reviews`, `category`, and `address`. The agent looks for:
- Libraries (public or university, if accessible)
- Cafes with high ratings (>4.2) and keywords like "quiet", "study-friendly" in reviews
- Co-working spaces

**Step 5 – Location Details (`browse_website` + `google_search`)**  
For promising study spots:
- Calls `browse_website` on their websites to check: *"free WiFi", "power outlets", "no time limit", "quiet environment"*
- Issues `google_search` queries like: *"<cafe name> Tsim Sha Tsui study friendly review"* to read user experiences about noise level and laptop usage policies.

**Step 6 – Equipment Shopping (`google_shopping`)**  
The agent makes multiple shopping calls:
- `query = "machine learning textbook hands-on Hong Kong"` → finds books like "Hands-On Machine Learning" (~HK$400)
- `query = "external hard drive 2TB Hong Kong"` → finds drives (~HK$600-800)
- `query = "portable monitor 15.6 inch Hong Kong"` → finds monitors (~HK$1200-1600)
- `query = "USB-C hub multiport"` → finds hubs (~HK$200-300)

The agent calculates total cost to stay within HK$3000 budget, prioritizing essential items.

**Step 7 – Product Review Check (`google_search`)**  
For high-value items (monitor, hard drive):
- Searches: *"<product model> review Hong Kong reliability"*
- Checks snippets for common issues: *"screen quality", "data transfer speed", "build quality"*

**Step 8 – Final Comprehensive Plan (no further tools)**  
The agent outputs:
- **Literature**: 5 papers with summaries and suggested reading order (foundational concepts → advanced techniques).
- **Study Locations**: 2-3 places with addresses, ratings, amenities (WiFi, outlets, noise level), and Maps links.
- **Equipment**: Itemized list with products, prices, purchase links, and total cost.

### 2.4 Correctness and Failure Analysis

**Overall outcome:**  
The agent successfully provides a holistic project preparation plan:
- `google_scholar` ensures relevant and high-quality literature.
- `google_maps_search` identifies practical study locations with real user ratings.
- `google_shopping` delivers budget-conscious equipment recommendations.

**Limitations and possible errors:**
- Some cafe websites are image-heavy or JavaScript-based; `browse_website` may miss detailed amenity information, forcing reliance on potentially incomplete Maps data.
- "Quiet" is subjective; even with reviews mentioning it, actual noise levels vary by time of day. The agent cannot guarantee a consistently quiet environment.
- Equipment prices fluctuate; the recommended budget breakdown is a snapshot and may not reflect current promotions or stock-outs.
- Very recent papers (e.g., published in the last 3 months) may not yet have enough citations to be surfaced by Scholar's default ranking, potentially causing the agent to miss cutting-edge work.

Nevertheless, the agent substantially automates the multi-step process of literature review, location scouting, and equipment procurement, saving hours of manual searching.

---

## Task 3 – Preparing for Thesis Defense Presentation

### 3.1 Real-World Manual Workflow

When I need to prepare for my undergraduate thesis defense, I would:

- Use Google Scholar to find recent papers that support my arguments or provide alternative perspectives on my research topic.
- Read abstracts and key findings to incorporate them into my defense slides and responses to potential questions.
- Use Google Maps to find professional printing and binding services near campus for my thesis copies and poster printing.
- Check reviews for print quality, turnaround time, and pricing.
- Shop for defense essentials: formal attire (suit or dress), presentation clicker/laser pointer, professional folders for thesis copies, USB backup drives.
- Compare prices and read reviews on e-commerce platforms to ensure quality within budget.

### 3.2 Agent Configuration and Tools Used

To automate this with my agent, I configure:

- `SearchAgent(use_tools=True, use_browsing=True, use_shopping=True, enable_maps=True, enable_scholar=True)`

The main tools used:

- `google_scholar` – to find supporting research papers for the defense.
- `google_maps_search` – to find printing and binding services near campus.
- `google_shopping` – to purchase defense essentials (attire, presentation tools, supplies).
- `google_search` & `browse_website` – auxiliary tools for print shop details and product specifications.

### 3.3 Agent Trajectory (≥ 5 Steps, ≥ 3 Tools)

**Step 1 – Initial Reasoning (no tool)**  
The user asks: *"I'm defending my undergraduate thesis on 'Graph Neural Networks for Molecular Property Prediction' next week. Please: (1) find 3-5 recent papers on GNN applications in chemistry to strengthen my literature review, (2) find 2-3 printing shops near HKUST for thesis binding and poster printing, and (3) suggest what I should buy for the defense with a budget of HK$2500."*

The agent identifies:
- Research topic: *Graph Neural Networks, molecular property prediction*
- Location: *Near HKUST (Hong Kong University of Science and Technology)*
- Budget: *HK$2500 for defense preparation*
- Tasks: *literature strengthening + printing services + shopping for essentials*

**Step 2 – Literature Search (`google_scholar`)**  
  The agent calls:
- Function: `google_scholar`
- Arguments:
  - `query = "graph neural networks molecular property prediction"`
    - `num = 20`  
  - `year_low = 2022`

Returns papers with `title`, `authors`, `year`, `cited_by`, `pdf_link`. The agent filters for:
- Recent publications (2022-2024)
- High citation count (>50 for recent papers, >100 for older ones)
- Relevant to GNN applications in chemistry/drug discovery
- Papers from top venues (Nature, Science, NeurIPS, ICML, etc.)

**Step 3 – Paper Abstract Reading (`browse_website`)**  
For the top 5 selected papers:
- Calls `browse_website` on `pdf_link` (typically arXiv or publisher sites).
- Extracts abstracts and key contributions.
- Summarizes findings: *"This paper introduces a novel message-passing framework for predicting quantum mechanical properties...", "Proposes an attention-based GNN architecture that achieves state-of-the-art on MoleculeNet benchmarks..."*
- Notes which papers could strengthen specific sections of the defense (methodology, related work, future directions).

**Step 4 – Printing Service Search (`google_maps_search`)**  
The agent calls:
- Function: `google_maps_search`
- Arguments:
  - `query = "printing shop thesis binding poster printing"`
  - `location = "Clear Water Bay, Hong Kong"` (near HKUST)
  - `num = 15`

Returns print shops with `rating`, `reviews`, `address`, `phone`. The agent filters for:
- Rating > 4.2
- High review count (>30) indicating reliability
- Services mentioned: thesis binding, large format poster printing, express service
- Reasonable distance from HKUST (within 20 minutes travel)

**Step 5 – Print Shop Details (`browse_website` + `google_search`)**  
For 2-3 promising print shops:
- Calls `browse_website` on their websites to check: *"thesis binding options (hardcover/softcover)", "poster printing sizes (A0, A1)", "turnaround time (express/standard)", "pricing"*
- Issues `google_search` like: *"<shop name> thesis binding quality review HKUST"* to find student experiences and feedback about print quality and reliability.

**Step 6 – Defense Essentials Shopping (`google_shopping`)**  
The agent makes multiple shopping queries:
- `query = "men formal suit Hong Kong"` → ~HK$800-1200 for business attire
- `query = "presentation clicker laser pointer wireless"` → ~HK$150-300
- `query = "leather document folder A4 professional"` → ~HK$100-200
- `query = "USB flash drive 64GB metal"` → ~HK$80-150
- `query = "portfolio presentation binder"` → ~HK$50-100

The agent calculates total cost to stay within HK$2500 budget, prioritizing:
- Formal attire (essential for professional appearance)
- Presentation clicker (improves delivery confidence)
- Document folders and backup drives (practical necessities)

**Step 7 – Product Review Verification (`google_search`)**  
For high-value items (formal suit, presentation clicker):
- Searches: *"<product model> review Hong Kong quality durability"*
- For suits: checks for *"fit", "fabric quality", "value for money"*
- For clickers: verifies *"Bluetooth range", "battery life", "compatibility with Mac/Windows"*

**Step 8 – Final Defense Preparation Plan (no further tools)**  
The agent outputs:
- **Literature Support**: 3-5 papers with titles, authors, key findings, and how they strengthen specific sections of the defense (e.g., "Paper A supports your methodology choice", "Paper B provides comparison benchmark").
- **Printing Services**: 2-3 print shops with addresses, ratings, services offered (thesis binding options, poster sizes), estimated costs, turnaround time, and booking phone numbers.
- **Defense Essentials**: Itemized shopping list with products, prices, purchase links, and total cost breakdown (~HK$2500).
  - Formal attire: HK$1000
  - Presentation clicker: HK$250
  - Document folders & USB drives: HK$200
  - Miscellaneous supplies: HK$100
  - Printing budget reserve: HK$950

### 3.4 Correctness and Failure Analysis

**Overall outcome:**  
The agent provides a comprehensive thesis defense preparation plan:
- `google_scholar` identifies relevant recent research to strengthen the literature review and provide talking points for potential committee questions.
- `google_maps_search` locates reliable printing services with student reviews, crucial for professional thesis presentation.
- `google_shopping` delivers practical recommendations for defense essentials within budget.

**Limitations and possible errors:**
- Scholar results may include papers that are topically related but not directly applicable to the specific thesis approach; the agent relies on titles/abstracts which may not fully capture relevance. Human judgment is still needed to select the most pertinent papers.
- Print shop pricing on Maps is often unavailable or outdated; actual thesis binding and poster printing costs require calling or visiting. The agent can identify candidates but cannot guarantee pricing accuracy.
- Formal attire sizing is highly personal; the agent can recommend stores/products but the user must verify fit in person. Online sizing charts help but aren't foolproof.
- Some print shops near universities offer student discounts not reflected in online listings; the agent may miss these cost-saving opportunities.
- Paper availability: some Scholar results may link to paywalled papers; students need institutional access to read full texts, which the agent cannot verify.

**Key strength:**  
Unlike Task 3's original fitness scenario, **preparing for thesis defense** is a realistic situation where students genuinely use Google Scholar (for last-minute literature checks), need local printing services (thesis copies and posters are mandatory for defense), and must purchase professional items. This workflow naturally combines all three tools in a coherent, time-sensitive task that students actually perform.

---

## Summary of the Three Tasks

- **Task 1 (Conference Preparation)** demonstrates **academic research + location planning + shopping**, using `google_scholar`, `google_maps_search`, and `google_shopping` in a realistic workflow for attending a professional event.

- **Task 2 (Course Project Preparation)** demonstrates **literature review + study location scouting + equipment procurement**, using the same three main tools for an academic project context.

- **Task 3 (Thesis Defense Preparation)** demonstrates **academic literature support + printing logistics + professional attire procurement**, using `google_scholar`, `google_maps_search`, and `google_shopping` in a high-stakes academic milestone context.

Each trajectory uses at least **three different main tools** (excluding search/browsing auxiliaries) and consists of at least **five steps**, closely mirroring realistic manual workflows while showing how the agent automates these processes end-to-end.

**Key Insight:**  
While `google_search` and `browse_website` are essential for gathering detailed information, the **core decision-making tools** (`google_scholar`, `google_maps_search`, `google_shopping`) drive the agent's ability to complete complex, multi-faceted real-world tasks that would otherwise require manually navigating multiple platforms and websites.
