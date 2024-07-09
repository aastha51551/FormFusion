from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.submission import SubmitFormRequest, SubmitFormResponse, submit_proto
from protocols.query import QueryFormRequest, QueryFormResponse, query_proto, FormStatus

# Create an agent named "organisation" on port 8001 with a specific seed phrase
organisation = Agent(
    name="organisation",
    port=8001,
    seed="org secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"],
)

# Fund the agent's wallet if the balance is low
fund_agent_if_low(organisation.wallet.address())

# Include the query and submission protocols
organisation.include(query_proto)
organisation.include(submit_proto)

# Define forms with their respective statuses
FORMS = {
    1: FormStatus(
        body="This is an internship application form",
        title="Internship Session",
        description="Form to apply for internship",
        fields=["Name", "Email", "Phone", "Resume"]
    ).dict(),
    2: FormStatus(
        body="This is a bug report form",
        title="Bug Report",
        description="Form to report software bugs",
        fields=["Name", "Email", "Bug Description", "Severity"]
    ).dict()
}

# Store the forms in the organisation's storage
for number, status in FORMS.items():
    organisation._storage.set(number, status)

# Run the agent
if __name__ == "__main__":
    organisation.run()
