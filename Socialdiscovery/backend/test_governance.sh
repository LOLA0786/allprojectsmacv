#!/bin/bash
set -e

BASE=http://127.0.0.1:8000

echo "1️⃣ Create Policy"
POLICY=$(curl -s -X POST $BASE/policies -d '{
  "scope":"hub:ai-governance",
  "rules":{
    "min_human_pct":0.6,
    "appeal":{"quorum":2}
  }
}')
POLICY_ID=$(echo $POLICY | jq -r .id)

echo "2️⃣ Create Intent"
INTENT=$(curl -s $BASE/intent)
INTENT_ID=$(echo $INTENT | jq -r .id)

echo "3️⃣ Create Cocreation"
CO=$(curl -s -X POST $BASE/cocreation/$INTENT_ID)
CO_ID=$(echo $CO | jq -r .id)

echo "4️⃣ Apply Veto"
VETO=$(curl -s -X PATCH $BASE/cocreation/$CO_ID/veto)
VETO_ID=$(echo $VETO | jq -r .veto_id)

echo "5️⃣ Submit Appeal"
APPEAL=$(curl -s -X POST $BASE/veto/$VETO_ID/appeal -d '{
  "argument":"Human expert review added",
  "requested_outcome":"revise",
  "author":"user_1"
}')
APPEAL_ID=$(echo $APPEAL | jq -r .id)

echo "6️⃣ Resolve Appeal"
curl -s -X POST $BASE/appeal/$APPEAL_ID/resolve -d '{"votes":2}'

echo "✅ GOVERNANCE FLOW COMPLETE"
