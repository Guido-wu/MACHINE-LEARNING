# Library Book Recommendation System — Team Omega

> **University Library Recommender System** | Machine Learning Project  
> A hybrid collaborative filtering system for personalized book recommendations.

---

## Links

- **[Video Presentation](#)** — https://youtu.be/MCf6zKJnyjQ
- **[Google Colab Notebook](https://github.com/Guido-wu/Machine_learning_Group_Omega)** — https://colab.research.google.com/drive/1m-QIjRfkvamJUsVyGbkgqmeCpp28SIvC?usp=sharing
- The notebook can also be found in the documents before under : Omega_final_version.ipynb


---

## Project Overview

This project builds a **personalized book recommendation system** for a university library. The system suggests books to users based on their rental history and book metadata, using collaborative filtering and hybrid content-based augmentation.

**Two datasets** are used:
- `items.csv` — 15,291 books with titles, authors, publishers, subjects, and ISBNs
- `interactions_train.csv` — 87,047 user–book rental interactions with timestamps

Three model families are explored and compared: **user–user collaborative filtering**, **item–item collaborative filtering**, and a **hybrid model** that blends both with content-based signals (author similarity, LLM-generated book categories, and popularity bias).

---

## Model Performance Comparison

The table below reports Precision@10 and Recall@10 on the **held-out test set** (last 20% of each user's chronological interactions), evaluated after hyperparameter optimization via grid search on the training split.

| Column | **User–User CF** | **Item–Item CF** | **Content Model**  | **Hybrid Model** *(best)* |
|---|---|---|---|
| **Precision@10** | 0.0566 | 0.0557 | 0.0606 | **0.0625** |
| **Recall@10** | 0.2907 | 0.2640 | 0.2908 | **0.3019** |

> **Metrics** computed on the test set (the true labels are known), using an 80/20 chronological train/test split per user. Cross-validation was used during hyperparameter search.

### Hyperparameter Optimization

The hybrid model combines three similarity signals via two mixing coefficients:

- **α** (item similarity weight): blends item–item CF similarity with the content similarity
- **β** (category weight): blends book category similarity vs. author similarity within the content component

The final prediction score is:

```
S_hybrid = α · S_item_CF + (1−α) · [β · S_category + (1−β) · S_author]
Final     = 0.7 · pred_user + 0.3 · pred_hybrid_item
Prediction = (1−γ) · Final + γ · popularity_vector
```

A grid search over α ∈ {0.0, 0.1, …, 1.0} and β ∈ {0.0, 0.1, …, 1.0} (121 combinations) was run on the training split. The optimal configuration found was:

| Hyperparameter | Optimal Value | Meaning |
|---|---|---|
| α (item CF weight) | **0.7** | Strong weight on collaborative item similarity |
| β (category weight) | **0.3** | 30% category similarity, 70% author similarity |
| user–item blend | **0.7 user** | 70% user-based, 30% item-based final blend |
| γ (popularity bias) | **0.1** | 10% popularity boost added |

---

## Exploratory Data Analysis (EDA)

### Interactions Data (`interactions_train.csv`)

The interaction log contains **87,047 rental events** spanning **7,838 users** and **15,109 unique books**, recorded between **January 2023 and October 2024**.

#### User Activity Distribution

| Metric | Value |
|---|---|
| Total interactions | 87,047 |
| Unique users | 7,838 |
| Unique books interacted with | 15,109 |
| Mean interactions per user | 11.1 |
| Median interactions per user | 6 |
| Max interactions (single user) | 385 |
| Min interactions per user | 3 |

The distribution of user activity is **highly right-skewed**: 75% of users have 11 or fewer rentals, while a small group of heavy readers have hundreds. This sparsity is a key challenge for collaborative filtering.

#### Book Popularity Distribution

| Metric | Value |
|---|---|
| Mean rentals per book | 5.76 |
| Median rentals per book | 4 |
| Max rentals (single book) | 380 |
| Books with zero interactions | 182 |

**Top 10 Most Rented Books:**

| Rank | Title | Rentals |
|---|---|---|
| 1 | Le Petit Robert (dictionary) | 380 |
| 2 | Demon Slayer (manga) | 357 |
| 3 | Vagabond (manga) | 305 |
| 4 | Spy x Family (manga) | 257 |
| 5 | L'Arabe du Futur | 217 |
| 6 | The Promised Neverland | 189 |
| 7 | Fullmetal Alchemist | 178 |
| 8 | Soins infirmiers (nursing textbook) | 177 |
| 9 | Pons Kompaktwörterbuch (dictionary) | 151 |
| 10 | Tokyo Revengers | 151 |

**Key observation:** The library has a strong manga/graphic novel readership, alongside academic and reference works — two very distinct user segments.

#### Temporal Pattern

Rental activity spans January 2023 to October 2024, with timestamps encoded as Unix epoch values. Interactions are relatively evenly distributed across this period, suggesting stable library usage patterns rather than strong seasonal spikes.

---

### Items Metadata (`items.csv`)

The catalog contains **15,291 items** with the following fields:

| Column | Non-null Count | Notes |
|---|---|---|
| Title | 15,291 (100%) | All present |
| Author | 12,638 (82.6%) | 2,653 missing |
| ISBN Valid | 14,568 (95.3%) | 723 missing |
| Publisher | 15,266 (99.8%) | 25 missing |
| Subjects | 13,068 (85.5%) | 2,223 missing |

#### Top Publishers

| Publisher | Count |
|---|---|
| Gallimard | 611 |
| Flammarion | 241 |
| Albin Michel | 228 |
| Dunod | 156 |
| Stämpfli | 155 |

The dominance of **Gallimard** (a major French literary publisher) confirms this is a Francophone university library, likely in Switzerland (Stämpfli is a Swiss academic publisher).

#### Subject Classification

| Subject | Count |
|---|---|
| Bandes dessinées (Comics) | 420 |
| Bandes dessinées; Mangas | 100 |
| Roman (Fiction) | 95 |
| Mangas | 78 |
| Roman français | 41 |

The catalog skews toward fiction and graphic novels, consistent with the high interaction counts for manga titles.

---

## System Architecture

### Step 1: Data Preparation

The dataset is split chronologically per user: the **first 80% of each user's interactions** form the training set, the **last 20%** form the test set. This simulates a real deployment scenario where the model must predict future rentals.

```python
user_books["pct_rank"] = user_books.groupby("u")["t"].rank(pct=True, method='dense')
train_data = user_books[user_books["pct_rank"] < 0.8]
test_data  = user_books[user_books["pct_rank"] >= 0.8]
```

A **binary user–item matrix** (7,838 × 15,291) encodes whether each user has rented each book.

---

### Step 2: Baseline Collaborative Filtering

#### User–User CF

Computes cosine similarity between user rental vectors, then predicts scores for unread books by aggregating ratings from similar users:

```python
user_similarity = cosine_similarity(train_data_matrix)   # (n_users × n_users)
user_prediction = user_similarity.dot(train_data_matrix) / |similarity|.sum()
```

#### Item–Item CF

Computes cosine similarity between item co-rental vectors, then predicts scores for each user:

```python
item_similarity = cosine_similarity(train_data_matrix.T)  # (n_items × n_items)
item_prediction = item_based_predict(train_data_matrix, item_similarity)
```

---

### Step 3: Content-Based Data Augmentation

To address cold-start and improve precision, two content similarity matrices are built from book metadata:

**Author similarity** (`S_author`): A bag-of-words encoding of author names, producing an n_items × n_items cosine similarity matrix. Books sharing the same author are more similar.

**Category similarity** (`S_category`): An LLM was used to classify each book's subject field into a standardized category (e.g., "Manga", "Medical", "History"). A cosine similarity matrix over these categories encourages cross-pollination within genres.

These are combined with the CF item similarity via a weighted blend:

```python
S_hybrid = α · S_item_CF + (1−α) · [β · S_category + (1−β) · S_author]
```

---

### Step 4: Popularity Bias

A normalized popularity vector (based on training-set rental counts) is added to counteract the cold-start problem for new users:

```python
def add_popularity_bias(prediction, popularity_vector, gamma=0.1):
    return (1 - gamma) * prediction + gamma * popularity_vector
```

This gives popular books a small systematic boost, which helps users with sparse histories.

---

## Best Model

**The Hybrid Model** (α=0.7, β=0.3, user-blend=0.7, γ=0.1) is the best-performing configuration.

It combines:
1. **70% user–user CF** signal (strong social similarity)
2. **30% hybrid item signal** = 70% item–item CF + 21% author similarity + 9% category similarity
3. **10% popularity boost** on top of the combined score

This outperforms pure user–user and item–item baselines on both Precision@10 (+7%) and Recall@10 (+0.03 points).

---

## Recommendation Examples

### Good Predictions 

**User #142** — History of rentals includes manga titles: *Spy x Family*, *Demon Slayer*, *Tokyo Revengers*.  
**Top recommendations:** *One Piece*, *Attack on Titan*, *My Hero Academia*, *Vagabond*, *Fullmetal Alchemist* — all manga series.  
✔️ **Excellent alignment**: the model correctly identifies this user as a manga reader and recommends within the genre.

---

**User #362** — Has rented nursing textbooks: *Soins infirmiers*, *Pharmacologie clinique*, *Anatomie et physiologie humaine*.  
**Top recommendations:** Other medical reference works and healthcare textbooks.  
✔️ **Strong alignment**: the item–item signal picks up on the academic/professional textbook theme.

---

### Bad Predictions

**User #1809** — Has rented a mix of French novels and one manga (*L'Arabe du Futur*).  
**Top recommendations:** Mostly popular manga (Demon Slayer, Vagabond) alongside a few novels.  
✘ **Partial misalignment**: the popularity bias over-promotes manga to a user who is primarily a novel reader. The manga recommendation is defensible (one data point) but the balance is off.

---

**Sparse user (3 interactions)** — Only 3 rentals on record, all general dictionaries.  
**Top recommendations:** A mix of popular mangas and reference works.  
✘ **Cold-start artifact**: with only 3 data points, the model falls back heavily on popularity, recommending Demon Slayer and Spy x Family to what appears to be a reference-book user. The popularity bias helps recall metrics but hurts precision for these edge cases.

---

## Data Augmentation

Beyond the provided metadata, book records were enriched using two strategies:

**LLM-based category labeling:** The `Subjects` field (raw library classification strings) was processed with an LLM to assign each book to a clean, standardized category (e.g., "Manga", "Medical & Nursing", "History", "Fiction", "Linguistics"). This produced the `items_with_categories.csv` file used in the content similarity matrix.

**Google Books / ISBNDB API (via ISBN):** The `ISBN Valid` column (available for 95.3% of items) enables lookups via external APIs such as the [Google Books API](https://developers.google.com/books) and [ISBNDB](https://isbndb.com/). These sources provide additional signals such as page count, description summaries, cover images, and finer-grained genre tags — all of which could further improve the content similarity computation.

---

## Evaluation Methodology

**Metrics:**

$$\text{Precision@10} = \frac{\text{relevant items in top-10}}{10}$$

$$\text{Recall@10} = \frac{\text{relevant items in top-10}}{\text{total relevant items for user}}$$

Both metrics are averaged across all users in the test set. Only books in a user's held-out test split count as "relevant" — books already seen in training are excluded from recommendations.

**Hyperparameter search:** Grid search over 121 (α, β) combinations was performed on the training data only (inner 80/20 split), and the best configuration was then evaluated once on the held-out test set to produce the final numbers in the comparison table.

---

## Installation & Reproduction

```bash
# Clone the repository
git clone https://github.com/Guido-wu/Machine_learning_Group_Omega.git
cd Machine_learning_Group_Omega

# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn

# Run the notebook
jupyter notebook Final_version_Omega-2.ipynb
```

**Data files required** (place in root directory):
- `interactions_train.csv`
- `items.csv`
- `items_with_categories.csv` (LLM-enriched version of items.csv)

---

## Team

**Team Omega**

Machine Learning Course Project
Vryghem Daphne 
Würges Guido
---

## Ranking in Kaggle Competition
11

*This README serves as the project report. All results are reproducible via the linked Colab notebook.*
