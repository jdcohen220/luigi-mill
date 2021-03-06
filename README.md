# Luigi / Papermill for Orchestrating Notebook-based tasks

## Overview
As a Data Engineering team that builds pipelines between systems and helps Data Scientists deploy models into production, we often have to 
collaborate with other teams when it comes to performing analyses or investigating anomalies on our data. As a result,
we hoped to explore options such as those used at [Netflix](https://medium.com/netflix-techblog/notebook-innovation-591ee3221233)
that are notebook based.

## Luigi
We currently use [Luigi](https://luigi.readthedocs.io/en/stable/) for our batch pipeline orchestration. Luigi is a Python  package that helps you build complex pipelines of batch jobs. It handles dependency resolution, workflow management, visualization, handling failures, command line integration, and much more.

## Papermill
We decided to test [Papermill](https://github.com/nteract/papermill), which is a tool for parameterizing, executing, and analyzing Jupyter Notebooks.

## Requirements
We used the following setup for our POC
* Container-based Jupyter from `jupyter/docker-stacks`.
* `papermill==0.15.1`
* `luigi==2.7.9`

## Putting It All Together
We discovered we could still use Luigi to orchestrate/resolve dependencies among different tasks that could be executed in a Jupyter notebook
by using the Papermill Python API from within a Luigi `run()` method. As a very basic example:

```python
import papermill as pm 
import luigi

class TestTask(luigi.Task):

	input_filename = luigi.Parameter()
	date = luigi.DateParameter()

	def run(self):

		pm.execute_notebook(
   			'template_notebook.ipynb',
   			'output_notebook_run_{0}.ipynb'.format(self.date),
   		parameters = dict(filename=self.input_filename, output_file='output_{0}.txt'.format(self.date))
		)
```

## Examples

* `template_notebook.ipynb` : Shows how to set default parameters in the cell `tag` and how to log (record) output to a dataframe.
* `example_output_notebook_2018-10-30.ipynb` : Example of a notebook run after being passed Luigi parameters.
* `example_output_with_exception_2018-09-02.ipynb` : Shows how a notebook that raises an Exception is written out. We were able to use this to confirm that a notebook with errors will signal a failure in the Luigi task pipleine.
* `example_explore_nb_dataframe.ipynb` : Demonstration of how to explore the output of an output notebook from a separate notebook.


