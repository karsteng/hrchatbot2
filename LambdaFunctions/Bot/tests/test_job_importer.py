from Bot import job_importer
from .utilities import get_fixture


def test_parse():
    html_job_response = get_fixture("job_response.txt")
    jobs = list(job_importer.parse_jobs(html_job_response))

    assert len(jobs) == 10
    assert jobs[0]["job_id"] == "link_1152488_1"
    assert jobs[9]["job_id"] == "link_1152488_10"


def test_parse_no_jobs():
    html_job_response = get_fixture("no_jobs_response.txt")
    jobs = list(job_importer.parse_jobs(html_job_response))

    assert len(jobs) == 0
