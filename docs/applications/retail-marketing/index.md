---
status: draft
last_reviewed: 2026-10-28
related:
  - theory/paradigms/online/contextual-bandits
  - theory/paradigms/supervised/trees-and-ensembles
  - society/ethics
aliases:
  - 零售、行銷與電子商務
  - Retail
  - E-commerce
---

# Retail, Marketing and E-commerce

Retail was one of the first industries to run large-scale machine learning on customer data. Recommendations, demand forecasts, pricing and advertising now shape most online shopping, and generative tools are adding product descriptions and campaign content. This page covers AI in selling and marketing products and services.

## Landscape

| Area | Examples |
|---|---|
| Recommendations | Suggesting products from browsing and purchase history |
| Demand forecasting | Predicting sales to plan stock and logistics |
| Pricing and promotions | Setting prices and discounts, sometimes dynamically |
| Customer retention | Predicting which customers are likely to leave |
| Advertising | Choosing which ad to show to which user |
| Content generation | Drafting product descriptions, emails and campaign copy |

## Recommendations and demand

Item-based collaborative filtering was an early, widely used approach. It finds relationships between items from a matrix of user ratings and then recommends items related to those a customer already likes (Sarwar et al., 2001). Amazon's item-to-item system is a well-known industrial example (Linden et al., 2003). Demand forecasting and price optimisation for an online retailer are analysed in Ferreira et al. (2016).

## Customer churn

Predicting which customers will leave is a standard supervised problem. Bagging and boosting of classification trees is one set of methods used for it (Lemmens & Croux, 2006). Retention offers then need to be targeted, which links the prediction to a decision about who gets a discount.

## Service and generative AI

Huang & Rust (2018) discuss how AI is changing service work. Generative tools now produce much of the marketing copy, which raises questions about brand voice, disclosure and quality control.

## Key methods

Three methods are most relevant. Each links to the page that explains it.

- [Trees and ensembles](../../theory/paradigms/supervised/trees-and-ensembles/index.md): the models behind churn prediction and many forecasting systems.
- [Contextual bandits](../../theory/paradigms/online/contextual-bandits/index.md): choosing which offer or ad to show, learning from the results as they arrive.
- [Evaluation and validation](../../theory/paradigms/supervised/evaluation-and-validation/index.md): testing whether a recommendation or price change actually increases sales, through controlled experiments.

## Risks

- **Manipulation.** Personalised pricing and nudging can exploit customers, and disclosure rules vary by country.
- **Privacy.** Behavioural data is central to these systems, so consent and retention policies matter.
- **Feedback loops.** Recommendations can narrow what customers see, reducing discovery.

Fairness and consumer-protection concerns are covered in [Ethics & Fairness](../../society/ethics/index.md).

## Open questions

- How much of the sales lift from recommendations is caused by the system, rather than by customers who would have bought anyway?
- How should personalised pricing be disclosed and limited?
- What happens to small retailers that cannot afford comparable data systems?

## References

### Seminal papers

- Sarwar, B. et al. (2001). Item-based Collaborative Filtering Recommendation Algorithms. *WWW10*. https://archives.iw3c2.org/www10/cdrom/papers/519/sdm2.html — Item-to-item methods that find relationships between items in a user–item rating matrix and use them to generate recommendations.
- Linden, G., Smith, B. & York, J. (2003). Amazon.com recommendations: item-to-item collaborative filtering. *IEEE Internet Computing*. https://doi.org/10.1109/MIC.2003.1167344 — Describes the item-to-item recommendation approach used by Amazon.com.
- Ferreira, K. J., Lee, B. H. A. & Simchi-Levi, D. (2016). Analytics for an Online Retailer: Demand Forecasting and Price Optimization. *Manufacturing & Service Operations Management* 18(1). https://doi.org/10.1287/msom.2015.0561 — Demand forecasting and price optimisation for an online retailer.
- Lemmens, A. & Croux, C. (2006). Bagging and Boosting Classification Trees to Predict Churn. *Journal of Marketing Research* 43(2). https://doi.org/10.1509/jmkr.43.2.276 — Uses bagging and boosting of classification trees to predict customer churn.

### Surveys and textbooks

- Huang, M.-H. & Rust, R. T. (2018). Artificial Intelligence in Service. *Journal of Service Research* 21(2). https://doi.org/10.1177/1094670517752459 — Discusses how AI is changing service work and the service industry.
