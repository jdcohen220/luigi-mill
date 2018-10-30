import papermill as pm 
import luigi

class TestTask(luigi.Task):
	"""
	A very basic example of how to execute a parameterized Jupyter Notebook
	by passing Luigi Parameters to a Papermill execution call.
	"""

	# The input filename to insert into the template notebook.
	input_filename = luigi.Parameter()
	# The date of the particular run
	date = luigi.DateParameter()

	def run(self):
		"""
		Execute template notebook with Luigi Parameters
		"""

		pm.execute_notebook(
   			'template_notebook.ipynb',
   			'parameterized_output_notebook_{0}.ipynb'.format(self.date),
   		parameters = dict(filename=self.input_filename, output_file='output_{0}.txt'.format(self.date))
		)

		# write to self.output to signal end of task/pipeline

		with self.output().open('w') as out_file:
			out_file.write('done')

	def output(self):
		"""
		Arbitrary output file to track Luigi Task completion.
		"""
		return luigi.LocalTarget('marker_file_{0}.txt'.format(self.date))