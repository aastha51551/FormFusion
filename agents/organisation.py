from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from protocols.submission import submit_proto, SubmitFormRequest, SubmitFormResponse
from protocols.query import query_proto, QueryFormRequest, QueryFormResponse, FormStatus

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
    ).dict()
}

# Store the forms in the organisation's storage
for number, status_dict in FORMS.items():
    organisation._storage.set(number, status_dict)

# Handle form submission requests
@organisation.on_message(SubmitFormRequest)
async def handle_submit_request(ctx: Context, sender: str, msg: SubmitFormRequest):
    form_status = organisation._storage.get(msg.title)
    if form_status:
        # Validate form fields (example: check if all fields are non-empty)
        if all(msg.fields):
            # Store submission data
            submission_data = {
                'title': msg.title,
                'fields': msg.fields
            }
            # Example: Store submission data in the agent's storage
            # Replace with your actual storage mechanism
            submission_id = await store_submission_data(ctx, submission_data)
            
            # Send success response
            await ctx.send(sender, SubmitFormResponse(success=True))
        else:
            # Incomplete fields, send failure response
            await ctx.send(sender, SubmitFormResponse(success=False))
    else:
        # Form not found, send failure response
        await ctx.send(sender, SubmitFormResponse(success=False))

async def store_submission_data(ctx: Context, submission_data: dict) -> str:
    # Example: Store submission data in agent's storage or database
    submission_id = f"submission_{ctx.message_id}"
    organisation._storage.set(submission_id, submission_data)
    return submission_id

if __name__ == "__main__":
    organisation.run()
