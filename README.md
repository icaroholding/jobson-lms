<div align="center" markdown="1">

<img src=".github/lms-logo.png" alt="Jobson Academy logo" width="80" height="80"/>
<h1>Jobson Academy</h1>

**Easy to use, open source, Learning Management System**

</div>


<div align="center">
	<img src=".github/hero.png?v=5" alt="Hero Image" width="72%" />
</div>

## Jobson Academy
Jobson Academy is an easy-to-use learning system that helps you bring structure to your content.

### Key Features

- **Structured Learning**: Design a course with a 3-level hierarchy, where your courses have chapters and you can group your lessons within these chapters. This ensures that the context of the lesson is set by the chapter.

- **Live Classes**: Group learners into batches based on courses and duration. You can then create Zoom live class for these batches right from the app. Learners get to see the list of live classes they have to take as a part of this batch.

- **Quizzes and Assignments**: Create quizzes where questions can have single-choice, multiple-choice options, or can be open ended. Instructors can also add assignments which learners can submit as PDF's or Documents.

- **Getting Certified**: Once a learner has completed the course or batch, you can grant them a certificate. The app provides an inbuilt certificate template. You can use this or else create a template of your own and use that instead.

<details>
<summary>View Screenshots</summary>


![Batch](.github/batch.png)
<div align="center">
	<sub>
		Create batches to group your learners
	</sub>
</div>
<br>


![Quiz](.github/quiz.png)
<div align="center">
	<sub>
		Evaluate their knowledge by quizzes
	</sub>
</div>
<br>


![Cerficicate](.github/certificate.png)
<div align="center">
	<sub>
		Autenticate their work with certification
	</sub>
</div>
</details>


### Under the Hood

- [**Frappe Framework**](https://github.com/frappe/frappe): A full-stack web application framework.
- [**Frappe UI**](https://github.com/frappe/frappe-ui): A Vue-based UI library, to provide a modern user interface.

## Development Setup

### Docker

You need Docker, docker-compose and git setup on your machine. Refer [Docker documentation](https://docs.docker.com/). After that, follow below steps:

**Step 1**: Setup folder and download the required files

    mkdir jobson-academy
    cd jobson-academy

    # Download the docker-compose file
    wget -O docker-compose.yml https://raw.githubusercontent.com/icaroholding/jobson-lms/develop/docker/docker-compose.yml

    # Download the setup script
    wget -O init.sh https://raw.githubusercontent.com/icaroholding/jobson-lms/develop/docker/init.sh

**Step 2**: Run the container and daemonize it

    docker compose up -d

**Step 3**: The site [http://lms.localhost:8000/lms](http://lms.localhost:8000/lms) should now be available. The default credentials are:
- Username: Administrator
- Password: admin

### Local

To setup the repository locally follow the steps mentioned below:

1. Install bench and setup a `frappe-bench` directory by following the [Installation Steps](https://frappeframework.com/docs/user/en/installation)
1. Start the server by running `bench start`
1. In a separate terminal window, create a new site by running `bench new-site learning.test`
1. Map your site to localhost with the command `bench --site learning.test add-to-hosts`
1. Get the app. Run `bench get-app https://github.com/icaroholding/jobson-lms`
1. Run `bench --site learning.test install-app lms`.
1. Now open the URL `http://learning.test:8000/lms` in your browser, you should see the app running

## License

AGPL-3.0-or-later

<br>
<div align="center" style="padding-top: 0.75rem;">
	<a href="https://bouncyloop.com" target="_blank">
		Powered by Bouncyloop
	</a>
</div>
