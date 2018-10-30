import papermill as pm 
import luigi

class TestTask(luigi.Task):

	input_filename = luigi.Parameter()
	date = luigi.DateParameter()

	def run(self):

		pm.execute_notebook(
   			'Pipeline POC.ipynb',
   			self.output().path,
   		parameters = dict(filename=self.input_filename, output_file='output_{0}.txt'.format(self.date))
		)

		with self.output().open('w') as out_file:
			out_file.write('done')

	def output(self):
		return luigi.LocalTarget('test_target_output_{0}.ipynb'.format(self.date))