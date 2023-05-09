headers = {
    "Content-Type": "application/json",
}

all_custom_fields = [
    "new_issue",
    "follow_up_issue",
    "not_an_issue",
    "reopen_after_autoclose",
    "not_a_reopen",
    "reopen_issue_resolved_additonal_info",
    "no update needed",
]

load = {"ticket": {}}

base_url = "https://hevodata.zendesk.com/api/v2/tickets/{}.json"

additional_tag = "reopen_validated"
# Reason for First reopen - 10343390026649
custom_fields = [{"id": 10343390026649}]

payload = ""

# ticket_id = 38961
# custom_field = "new_issue"


recipient_emails = [
    "anu.yadav@hevodata.com",
    "arun.sunderraj@hevodata.com",
    "chirag.agarwal@hevodata.com",
    "dimple.mk@hevodata.com",
    "dipak.patil@hevodata.com",
    "geetha.n@hevodata.com",
    "kamlesh.chhipa@hevodata.com",
    "karthic.c@hevodata.com",
    "madhusudhan.gaddam@hevodata.com",
    "monica.patel@hevodata.com",
    "mridul.juyal@hevodata.com",
    "muskan.kesharwani@hevodata.com",
    "nathaniel.rampur@hevodata.com",
    "nishant.tandon@hevodata.com",
    "nitin.birajdar@hevodata.com",
    "prashant@hevodata.com",
    "rohit.guntuku@hevodata.com",
    "sai.rao@hevodata.com",
    "sarthak.bhardwaj@hevodata.com",
    "sasikumar.reddy@hevodata.com",
    "satyam.agrawal@hevodata.com",
    "sindhura.devarapalli@hevodata.com",
    "skand.agrawal@hevodata.com",
    "sneha.r@hevodata.com",
    "subham.bansal@hevodata.com",
    "sudhanshu.sharan@hevodata.com",
    "veeresh.biradar@hevodata.com",
    "vinita.mittal@hevodata.com",
    "vishnu.bhargav@hevodata.com" "akanksha.singh@hevodata.com",
    "anmol.baunthiyal@hevodata.com",
    "madanlal.bidiyasar@hevodata.com",
    "parthiv.patel@hevodata.com",
    "pushkar.dayal@hevodata.com",
    "rahul.kumar@hevodata.com",
    "raja.pandey@hevodata.com",
    "shivanshu.dabral@hevodata.com",
    "siddhartha.chauhan@hevodata.com",
]
