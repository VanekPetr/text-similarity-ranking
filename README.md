# Text Similarity Ranking for Numeric-rich Short Words

Welcome to our repository, where we delve into the intriguing world of text similarity ranking, specifically tailored for short words that feature a high density of numbers. This repository has been crafted to address the nuances involved in comparing and evaluating text strings that are not just alphabetic but are significantly numerical in nature. Our focus here is on implementing and advancing methodologies that excel in assessing the similarity of such strings, an endeavor that is crucial in many data processing and natural language processing (NLP) tasks today.

## Overview

In many real-world applications, from data cleaning in large databases to advanced NLP tasks, the need to accurately determine the similarity between text strings is paramount. This becomes particularly challenging when dealing with short words densely populated with numbers, as traditional text similarity metrics may fall short. Recognizing this gap, we introduce an implementation of the renowned Jaro-Winkler algorithm, tailored specifically for our use case. Furthermore, we take a step ahead with the introduction of the Jars-Winkler-Vanek (JWV) algorithm, a novel modification designed to enhance performance in our specific context.

## Jaro-Winkler Algorithm

The Jaro-Winkler algorithm is a well-established metric for measuring the similarity betweentwo text strings. Its efficiency in capturing the degree of match between data entries has made it a go-to choice for applications ranging from data mining to NLP. The algorithm focuses on the number and order of common characters between the strings, adjusting the similarity score based on the prefix length to give higher importance to strings that match from the beginning.

### Our Implementation

In this repository, we have implemented the Jaro-Winkler algorithm with a focus on optimizing it for short words that are abundant with numbers. This adaptation ensures that our approach is sensitive to the unique challenges presented by numerical-heavy strings, providing more accurate similarity assessments.

## Jaro-Winkler-Vanek (JWV) Algorithm

Building on the foundations of the Jaro-Winkler algorithm, we introduce the Jars-Winkler-Vanek (JWV) algorithm. This innovative modification is engineered to better handle our specific scenario: comparing short words with a significant numerical component.

### Key Features

- **Adaptive Matching**: The JWV algorithm extends the original metric by proposing a matching scheme that accounts for the number of words or, in the case of single words, the number of characters. This ensures a more nuanced similarity assessment that is better tuned to the characteristics of numeric-rich short words.
- **Enhanced Precision**: By adjusting the similarity scoring to consider the specific structure of the strings (i.e., word count or character count), the JWV algorithm offers a more precise measurement for our context, leading to more reliable outcomes.

## Use Cases

The methodologies presented in this repository are particularly useful for:
- Data cleaning and deduplication in databases where entries are short and contain numerous numbers.
- Similarity checks in cybersecurity for detecting suspiciously similar strings or codes.
- NLP tasks where precise similarity measures can significantly enhance the performance of algorithms dealing with short numeric strings, such as password strength evaluation or financial document analysis.

## Getting Started

STEP 1: create and activate python virtual environment
``` bash
python -m venv venv
source venv/bin/activate
```

STEP 2: install requirements with [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
``` bash
poetry install -vv
```

## **Usage**

Detailed usage instructions for implementing both the Jaro-Winkler and JWV algorithms are provided in the respective module documentation within the repository.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/VanekPetr/text-similarity-ranking/tags).


## License

This repository is licensed under [MIT](LICENSE) (c) 2023 GitHub, Inc.

<div align='center'>
<a href='https://github.com/VanekPetr/text-similarity-ranking/releases'>
<img src='https://img.shields.io/github/v/release/vanekpetr/text-similarity-ranking?color=%23FDD835&label=version&style=for-the-badge'>
</a>
<a href='https://github.com/VanekPetr/text-similarity-ranking/blob/main/LICENSE'>
<img src='https://img.shields.io/github/license/vanekpetr/text-similarity-ranking?style=for-the-badge'>
</a>
</div>
