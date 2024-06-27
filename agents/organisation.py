from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.submission import submit_proto
from protocols.query import query_proto, FormStatus
 
organisation = Agent(
    name="organisation",
    port=8001,
    seed="org secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)
 
fund_agent_if_low(organisation.wallet.address())
 
organisation.include(query_proto)
organisation.include(submit_proto)
FORMS = {
    
}

for (number, status) in FORMS.items():
    organisation._storage.set(number, status.dict())
 
if __name__ == "__main__":
    organisation.run()