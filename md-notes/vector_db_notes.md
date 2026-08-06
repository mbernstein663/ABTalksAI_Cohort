# Vector Database Notes, ABTalks Day 08

## ChromaDB vs. Pinecone Comparison

| Factor | ChromaDB | Pinecone |
| --- | --- | --- |
| Local vs. cloud | Local, self-hosted, or Chroma Cloud | Managed cloud service |
| Free tier | Local use limited only by hardware; Cloud gives $5 credits | 5 indexes, 2 GB storage, usage limits |
| Latency | Very low when running locally | Network latency, but production-scalable |
| Setup | Simple Python install and local folder | Account, API key, region, and index |
| Access control | Separate collections/tenants or metadata filters | Separate namespaces or metadata filters |
| Enterprise fit | Backend must enforce member and plan permissions | Backend must enforce namespace and plan permissions |

**Which will we use?**

For this project, **ChromaDB** seems like the more adequate choice. This is because this (for now) is an example RAG project that is not production grade. There is no "free tier" or usage subscription- and since I have strong hardware I shouldn't have much of a problem even if we do add more documents. The setup is simple and the code is understandable. Overall, the simplicity and locality of this project makes it the smarter choice.

## Vector Database Overview Notes

### Pinecone

A fully managed vector database for production RAG. Serverless indexes keep records in distributed object storage while Pinecone handles indexing, scaling, filtering, and availability.

- **Tradeoff:** minimal maintenance, but less infrastructure control, vendor dependence, and usage-based cost.
- **Use when:** you need production retrieval without operating database clusters.

### Chroma

An open-source, developer-friendly database for local applications and smaller RAG systems. Single-node Chroma stores documents and metadata in SQLite while its HNSW index resides in RAM; Chroma Cloud uses distributed services and object storage.

- **Tradeoff:** simple setup, but local deployments have lower scaling limits.
- **Use when:** prototyping, building internal tools, or learning RAG.

### FAISS

Meta’s similarity-search library, not a complete database. It provides Flat, IVF, HNSW, and compressed indexes, commonly using RAM or GPUs, and indexes can be saved to disk. It lacks built-in server management, authentication, replication, and rich metadata storage.

- **Tradeoff:** maximum algorithmic control, but you must build the surrounding system.
- **Use when:** developing custom retrieval engines or research pipelines.

### Weaviate

An open-source database supporting vector, keyword, hybrid, and filtered search. Each shard combines LSM-based object and inverted storage with a vector index such as HNSW.

- **Tradeoff:** strong schemas and hybrid retrieval, but more configuration and memory overhead than Chroma.
- **Use when:** production RAG requires structured metadata, filters, and keyword-vector search.

### Milvus

An open-source distributed database for large vector collections. It separates compute from storage: vectors and indexes persist in object storage, metadata is managed separately, and query nodes load searchable segments.

- **Tradeoff:** strong horizontal scaling, but greater deployment complexity.
- **Use when:** data volume or traffic justifies dedicated distributed infrastructure.

**Conclusion:** Chroma is the easiest local starting point; FAISS is the low-level engine for custom systems; Pinecone minimizes operations; Weaviate emphasizes hybrid retrieval and data modeling; and Milvus targets distributed scale. Choose based on required control, data size, filtering needs, and the infrastructure your team can realistically operate.

## Indexing Algorithms

A vector-database indexing algorithm organizes embeddings so similarity search avoids comparing a query with every stored vector. Similarity is commonly measured with cosine similarity,

$$
\cos(q,x)=\frac{q\cdot x}{|q||x|}
$$

or Euclidean distance, $$(|q-x|_2)$$

### HNSW

**HNSW: Hierarchical Navigable Small World**  builds a multi-layer proximity graph. Search starts in sparse upper layers, then moves through denser layers toward nearby vectors. It offers high recall and low latency, but uses more memory and takes longer to build. Works like a greedy local search with best-first or beam-like graph search.

```
Sparse upper graph → large movement

Denser middle graph → regional refinement

Full bottom graph → precise local search
```

Use HNSW for fast, high-quality retrieval on frequently queried datasets. 

### IVF

**IVF: Inverted File Index** partitions vectors into clusters (bucket labels), often using k-means:

$$
\min_{\mu_1,\dots,\mu_k}\sum_i \min_j |x_i-\mu_j|_2^2
$$

At query time, only the nearest clusters are searched. IVF uses less memory and scales well, but recall depends on cluster quality and how many partitions are probed.

- IVF-Flat: stores full vectors inside each cluster.
- IVF-PQ: compresses vectors using Product Quantization.
- IVF-SQ: compresses vectors using Scalar Quantization.

Use IVF for very large collections, tighter memory limits, or batch systems. Both trade exactness for speed: more graph exploration or cluster probes improves recall but increases latency.