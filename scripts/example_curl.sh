#!/bin/bash
curl -X POST "http://127.0.0.1:8000/api/summarize" -H "Content-Type: application/json" -d '{"doc_id":"sample_text","mode":"tldr"}'
