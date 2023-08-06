
.. This is an automatically generated file.
.. do not modify by hand.

Configuration options
=====================

Configuration options may be set in a file, ``~/.jupyter/jupyter_nbconvert_config.py``,
or at the command line when starting nbconvert, i.e. ``jupyter nbconvert --Application.log_level=10``.

The most specific setting will always be used. For example, the LatexExporter
and the HTMLExporter both inherit from TemplateExporter. With the following config

.. code-block:: python

    c.TemplateExporter.exclude_input_prompt = False # The default
    c.PDFExporter.exclude_input_prompt = True

input prompts will not appear when converting to PDF, but they will appear when
exporting to HTML.

CLI Flags and Aliases
---------------------

When using Nbconvert from the command line, a number of aliases and flags are
defined as shortcuts to configuration options for convience.

The following flags are defined:

debug
    set log level to logging.DEBUG (maximize logging output)

    Long Form: {'Application': {'log_level': 10}}

generate-config
    generate default config file

    Long Form: {'JupyterApp': {'generate_config': True}}

y
    Answer yes to any questions instead of prompting.

    Long Form: {'JupyterApp': {'answer_yes': True}}

execute
    Execute the notebook prior to export.

    Long Form: {'ExecuteProcessor': {'enabled': True}}

allow-errors
    Continue notebook execution even if one of the cells throws an error and include
    the error message in the cell output (the default behaviour is to abort
    conversion). This flag is only relevant if '--execute' was specified, too.

    Long Form: {'ExecuteProcessor': {'allow_errors': True}}

stdin
    read a single notebook file from stdin. Write the resulting notebook with
    default basename 'notebook.*'

    Long Form: {'NbConvertApp': {'from_stdin': True}}

stdout
    Write notebook output to stdout instead of files.

    Long Form: {'NbConvertApp': {'writer_class': 'StdoutWriter'}}

inplace
    Run nbconvert in place, overwriting the existing notebook (only
    relevant when converting to notebook format)

    Long Form: {'NbConvertApp': {'use_output_suffix': False, 'export_format':
    'notebook'}, 'FilesWriter': {'build_directory': ''}}

clear-output
    Clear output of current file and save in place,          overwriting the
    existing notebook.

    Long Form: {'NbConvertApp': {'use_output_suffix': False, 'export_format':
    'notebook'}, 'FilesWriter': {'build_directory': ''}, 'ClearOutputProcessor':
    {'enabled': True}}

no-prompt
    Exclude input and output prompts from converted document.

    Long Form: {'TemplateExporter': {'exclude_input_prompt': True,
    'exclude_output_prompt': True}}

no-input
    Exclude input cells and output prompts from converted document.          This
    mode is ideal for generating code-free reports.

    Long Form: {'TemplateExporter': {'exclude_output_prompt': True, 'exclude_input':
    True}}

The folowing aliases are defined:

	**log-level** (Application.log_level)

	**config** (JupyterApp.config_file)

	**to** (NbConvertApp.export_format)

	**template** (TemplateExporter.template_name)

	**template-file** (TemplateExporter.template_file)

	**writer** (NbConvertApp.writer_class)

	**post** (NbConvertApp.postprocessor_class)

	**output** (NbConvertApp.output_base)

	**output-dir** (FilesWriter.build_directory)

	**reveal-prefix** (SlidesExporter.reveal_url_prefix)

	**nbformat** (NotebookExporter.nbformat_version)


App Options
-----------------------

Application.log_datefmt \: Unicode
    Default: ``'%Y-%m-%d %H:%M:%S'``

    The date format used by logging formatters for %(asctime)s

Application.log_format \: Unicode
    Default: ``'[%(name)s]%(highlevel)s %(message)s'``

    The Logging format template

Application.log_level \: 0|10|20|30|40|50|'DEBUG'|'INFO'|'WARN'|'ERROR'|'CRITICAL'
    Default: ``30``

    Set the log level by value or name.

JupyterApp.answer_yes \: Bool
    Default: ``False``

    Answer yes to any prompts.

JupyterApp.config_file \: Unicode
    Default: ``''``

    Full path of a config file.

JupyterApp.config_file_name \: Unicode
    Default: ``''``

    Specify a config file to load.

JupyterApp.generate_config \: Bool
    Default: ``False``

    Generate default config file.

NbConvertApp.export_format \: Unicode
    Default: ``''``

    The export format to be used, either one of the built-in formats
    ['asciidoc', 'custom', 'html', 'latex', 'markdown', 'notebook', 'pdf', 'python', 'rst', 'script', 'slides']
    or a dotted object name that represents the import path for an
    `Exporter` class

NbConvertApp.from_stdin \: Bool
    Default: ``False``

    read a single notebook from stdin.

NbConvertApp.html_manager_semver_range \: Unicode
    Default: ``'*'``

    Semver range for Jupyter widgets HTML manager

NbConvertApp.jupyter_widgets_base_url \: Unicode
    Default: ``'https://unpkg.com/'``

    URL base for Jupyter widgets

NbConvertApp.notebooks \: List
    Default: ``[]``

    List of notebooks to convert.
    Wildcards are supported.
    Filenames passed positionally will be added to the list.


NbConvertApp.output_base \: Unicode
    Default: ``''``

    overwrite base name use for output files.
    can only be used when converting one notebook at a time.


NbConvertApp.output_files_dir \: Unicode
    Default: ``'{notebook_name}_files'``

    Directory to copy extra files (figures) to.
    '{notebook_name}' in the string will be converted to notebook
    basename.

NbConvertApp.postprocessor_class \: DottedOrNone
    Default: ``''``

    PostProcessor class used to write the
    results of the conversion

NbConvertApp.use_output_suffix \: Bool
    Default: ``True``

    Whether to apply a suffix prior to the extension (only relevant
    when converting to notebook format). The suffix is determined by
    the exporter, and is usually '.nbconvert'.

NbConvertApp.writer_class \: DottedObjectName
    Default: ``'FilesWriter'``

    Writer class used to write the 
    results of the conversion

Exporter Options
-----------------------

.. image:: _static/exporter_inheritance.png

Exporter.default_processors \: List
    Default: ``['nbconvert.processors.TagRemoveProcessor', 'nbconvert.proces...``

    List of processors available by default, by name, namespace,
    instance, or type.

Exporter.enabled \: Bool
    Default: ``True``

    Disable this exporter (and any exporters inherited from it).

Exporter.file_extension \: FilenameExtension
    Default: ``''``

    Extension of the file that should be written to disk

Exporter.processors \: List
    Default: ``[]``

    List of processors, by name or namespace, to enable.

TemplateExporter.exclude_code_cell \: Bool
    Default: ``False``

    This allows you to exclude code cells from all templates if set to True.

TemplateExporter.exclude_input \: Bool
    Default: ``False``

    This allows you to exclude code cell inputs from all templates if set to True.

TemplateExporter.exclude_input_prompt \: Bool
    Default: ``False``

    This allows you to exclude input prompts from all templates if set to True.

TemplateExporter.exclude_markdown \: Bool
    Default: ``False``

    This allows you to exclude markdown cells from all templates if set to True.

TemplateExporter.exclude_output \: Bool
    Default: ``False``

    This allows you to exclude code cell outputs from all templates if set to True.

TemplateExporter.exclude_output_prompt \: Bool
    Default: ``False``

    This allows you to exclude output prompts from all templates if set to True.

TemplateExporter.exclude_raw \: Bool
    Default: ``False``

    This allows you to exclude raw cells from all templates if set to True.

TemplateExporter.exclude_unknown \: Bool
    Default: ``False``

    This allows you to exclude unknown cells from all templates if set to True.

TemplateExporter.filters \: Dict
    Default: ``{}``

    Dictionary of filters, by name and namespace, to add to the Jinja
    environment.

TemplateExporter.raw_mimetypes \: List
    Default: ``[]``

    formats of raw cells to be included in this Exporter's output.

TemplateExporter.template_extension \: Unicode
    Default: ``'.tpl'``

    No description

TemplateExporter.template_file \: Unicode
    Default: ``None``

    Name of the template file to use

TemplateExporter.template_name \: Unicode
    Default: ``''``

    Name of the template to use

TemplateExporter.template_path \: List
    Default: ``['.']``

    No description


HTMLExporter.anchor_link_text \: Unicode
    Default: ``'¶'``

    The text used as the text for anchor links.

HTMLExporter.exclude_anchor_links \: Bool
    Default: ``False``

    If anchor links should be included or not.

HTMLExporter.jquery_url \: Unicode
    Default: ``'https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.m...``

    
    URL to load jQuery from.
    
    Defaults to loading from cdnjs.


HTMLExporter.require_js_url \: Unicode
    Default: ``'https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/req...``

    
    URL to load require.js from.
    
    Defaults to loading from cdnjs.


HTMLExporter.theme \: Unicode
    Default: ``'light'``

    Template specific theme(e.g. the JupyterLab CSS theme for the lab template)



NotebookExporter.nbformat_version \: 1|2|3|4
    Default: ``4``

    The nbformat version to write.
    Use this to downgrade notebooks.


PDFExporter.bib_command \: List
    Default: ``['bibtex', '{filename}']``

    Shell command used to run bibtex.

PDFExporter.latex_command \: List
    Default: ``['xelatex', '{filename}', '-quiet']``

    Shell command used to compile latex.

PDFExporter.latex_count \: Int
    Default: ``3``

    How many times latex will be called.

PDFExporter.verbose \: Bool
    Default: ``False``

    Whether to display the output of latex commands.




SlidesExporter.font_awesome_url \: Unicode
    Default: ``'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/cs...``

    
    URL to load font awesome from.
    
    Defaults to loading from cdnjs.


SlidesExporter.reveal_scroll \: Bool
    Default: ``False``

    
    If True, enable scrolling within each slide


SlidesExporter.reveal_theme \: Unicode
    Default: ``'simple'``

    
    Name of the reveal.js theme to use.
    
    We look for a file with this name under
    ``reveal_url_prefix``/css/theme/``reveal_theme``.css.
    
    https://github.com/hakimel/reveal.js/tree/master/css/theme has
    list of themes that ship by default with reveal.js.


SlidesExporter.reveal_transition \: Unicode
    Default: ``'slide'``

    
    Name of the reveal.js transition to use.
    
    The list of transitions that ships by default with reveal.js are:
    none, fade, slide, convex, concave and zoom.


SlidesExporter.reveal_url_prefix \: Unicode
    Default: ``''``

    The URL prefix for reveal.js (version 3.x).
    This defaults to the reveal CDN, but can be any url pointing to a copy 
    of reveal.js. 
    
    For speaker notes to work, this must be a relative path to a local 
    copy of reveal.js: e.g., "reveal.js".
    
    If a relative path is given, it must be a subdirectory of the
    current directory (from which the server is run).
    
    See the usage documentation
    (https://nbconvert.readthedocs.io/en/latest/usage.html#reveal-js-html-slideshow)
    for more details.


SlidesExporter.template_name \: Unicode
    Default: ``'reveal'``

    Name of the template to use

Writer Options
-----------------------

.. image:: _static/writer_inheritance.png

WriterBase.files \: List
    Default: ``[]``

    
    List of the files that the notebook references.  Files will be 
    included with written output.


FilesWriter.build_directory \: Unicode
    Default: ``''``

    Directory to write output(s) to. Defaults
    to output to the directory of each notebook. To recover
    previous default behaviour (outputting to the current 
    working directory) use . as the flag value.

FilesWriter.relpath \: Unicode
    Default: ``''``

    When copying files that the notebook depends on, copy them in
    relation to this path, such that the destination filename will be
    os.path.relpath(filename, relpath). If FilesWriter is operating on a
    notebook that already exists elsewhere on disk, then the default will be
    the directory containing that notebook.


Processor Options
-----------------------

.. image:: _static/processor_inheritance.png

Processor.enabled \: Bool
    Default: ``False``

    No description

CSSHTMLHeaderProcessor.highlight_class \: Unicode
    Default: ``'.highlight'``

    CSS highlight class identifier

CSSHTMLHeaderProcessor.style \: Union
    Default: ``<class 'jupyterlab_pygments.style.JupyterStyle'>``

    Name of the pygments style to use


ClearOutputProcessor.remove_metadata_fields \: Set
    Default: ``{'collapsed', 'scrolled'}``

    No description

ConvertFiguresProcessor.from_format \: Unicode
    Default: ``''``

    Format the converter accepts

ConvertFiguresProcessor.to_format \: Unicode
    Default: ``''``

    Format the converter writes


ExtractOutputProcessor.extract_output_types \: Set
    Default: ``{'image/png', 'image/svg+xml', 'application/pdf', 'image/jpeg'}``

    No description

ExtractOutputProcessor.output_filename_template \: Unicode
    Default: ``'{unique_key}_{cell_index}_{index}{extension}'``

    No description

HighlightMagicsProcessor.languages \: Dict
    Default: ``{}``

    Syntax highlighting for magic's extension languages. Each item associates a language magic extension such as %%R, with a pygments lexer such as r.

LatexProcessor.style \: Unicode
    Default: ``'default'``

    Name of the pygments style to use

RegexRemoveProcessor.patterns \: List
    Default: ``[]``

    No description

SVG2PDFProcessor.command \: Unicode
    Default: ``''``

    The command to use for converting SVG to PDF
    
    This string is a template, which will be formatted with the keys
    to_filename and from_filename.
    
    The conversion call must read the SVG from {from_filename},
    and write a PDF to {to_filename}.


SVG2PDFProcessor.inkscape \: Unicode
    Default: ``''``

    The path to Inkscape, if necessary

SVG2PDFProcessor.inkscape_version \: Unicode
    Default: ``''``

    The version of inkscape being used.
    
    This affects how the conversion command is run.


TagRemoveProcessor.remove_all_outputs_tags \: Set
    Default: ``set()``

    Tags indicating cells for which the outputs are to be removed,matches tags in `cell.metadata.tags`.

TagRemoveProcessor.remove_cell_tags \: Set
    Default: ``set()``

    Tags indicating which cells are to be removed,matches tags in `cell.metadata.tags`.

TagRemoveProcessor.remove_input_tags \: Set
    Default: ``set()``

    Tags indicating cells for which input is to be removed,matches tags in `cell.metadata.tags`.

TagRemoveProcessor.remove_single_output_tags \: Set
    Default: ``set()``

    Tags indicating which individual outputs are to be removed,matches output *i* tags in `cell.outputs[i].metadata.tags`.


ServePostProcessor.browser \: Unicode
    Default: ``''``

    Specify what browser should be used to open slides. See
    https://docs.python.org/3/library/webbrowser.html#webbrowser.register
    to see how keys are mapped to browser executables. If 
    not specified, the default browser will be determined 
    by the `webbrowser` 
    standard library module, which allows setting of the BROWSER 
    environment variable to override it.


ServePostProcessor.ip \: Unicode
    Default: ``'127.0.0.1'``

    The IP address to listen on.

ServePostProcessor.open_in_browser \: Bool
    Default: ``True``

    Should the browser be opened automatically?

ServePostProcessor.port \: Int
    Default: ``8000``

    port for the server to listen on.

ServePostProcessor.reveal_cdn \: Unicode
    Default: ``'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.5.0'``

    URL for reveal.js CDN.

ServePostProcessor.reveal_prefix \: Unicode
    Default: ``'reveal.js'``

    URL prefix for reveal.js

Postprocessor Options
-----------------------


ServePostProcessor.browser \: Unicode
    Default: ``''``

    Specify what browser should be used to open slides. See
    https://docs.python.org/3/library/webbrowser.html#webbrowser.register
    to see how keys are mapped to browser executables. If 
    not specified, the default browser will be determined 
    by the `webbrowser` 
    standard library module, which allows setting of the BROWSER 
    environment variable to override it.


ServePostProcessor.ip \: Unicode
    Default: ``'127.0.0.1'``

    The IP address to listen on.

ServePostProcessor.open_in_browser \: Bool
    Default: ``True``

    Should the browser be opened automatically?

ServePostProcessor.port \: Int
    Default: ``8000``

    port for the server to listen on.

ServePostProcessor.reveal_cdn \: Unicode
    Default: ``'https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.5.0'``

    URL for reveal.js CDN.

ServePostProcessor.reveal_prefix \: Unicode
    Default: ``'reveal.js'``

    URL prefix for reveal.js

Other Options
-----------------------




NbConvertBase.default_language \: Unicode
    Default: ``'ipython'``

    Deprecated default highlight language as of 5.0, please use language_info metadata instead

NbConvertBase.display_data_priority \: List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``

    
    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


NotebookClient.allow_errors \: Bool
    Default: ``False``

    
    If `False` (default), when a cell raises an error the
    execution is stopped and a `CellExecutionError`
    is raised.
    If `True`, execution errors are ignored and the execution
    is continued until the end of the notebook. Output from
    exceptions is included in the cell output in both cases.


NotebookClient.display_data_priority \: List
    Default: ``['text/html', 'application/pdf', 'text/latex', 'image/svg+xml...``

    
    An ordered list of preferred output type, the first
    encountered will usually be used when converting discarding
    the others.


NotebookClient.extra_arguments \: List
    Default: ``[]``

    No description

NotebookClient.force_raise_errors \: Bool
    Default: ``False``

    
    If False (default), errors from executing the notebook can be
    allowed with a `raises-exception` tag on a single cell, or the
    `allow_errors` configurable option for all cells. An allowed error
    will be recorded in notebook output, and execution will continue.
    If an error occurs when it is not explicitly allowed, a
    `CellExecutionError` will be raised.
    If True, `CellExecutionError` will be raised for any error that occurs
    while executing the notebook. This overrides both the
    `allow_errors` option and the `raises-exception` cell tag.


NotebookClient.interrupt_on_timeout \: Bool
    Default: ``False``

    
    If execution of a cell times out, interrupt the kernel and
    continue executing other cells rather than throwing an error and
    stopping.


NotebookClient.iopub_timeout \: Int
    Default: ``4``

    
    The time to wait (in seconds) for IOPub output. This generally
    doesn't need to be set, but on some slow networks (such as CI
    systems) the default timeout might not be long enough to get all
    messages.


NotebookClient.ipython_hist_file \: Unicode
    Default: ``':memory:'``

    Path to file to use for SQLite history database for an IPython kernel.
    
    The specific value `:memory:` (including the colon
    at both end but not the back ticks), avoids creating a history file. Otherwise, IPython
    will create a history file for each kernel.
    
    When running kernels simultaneously (e.g. via multiprocessing) saving history a single
    SQLite file can result in database errors, so using `:memory:` is recommended in
    non-interactive contexts.


NotebookClient.kernel_manager_class \: Type
    Default: ``'builtins.object'``

    The kernel manager class to use.

NotebookClient.kernel_name \: Unicode
    Default: ``''``

    
    Name of kernel to use to execute the cells.
    If not set, use the kernel_spec embedded in the notebook.


NotebookClient.raise_on_iopub_timeout \: Bool
    Default: ``False``

    
    If `False` (default), then the kernel will continue waiting for
    iopub messages until it receives a kernel idle message, or until a
    timeout occurs, at which point the currently executing cell will be
    skipped. If `True`, then an error will be raised after the first
    timeout. This option generally does not need to be used, but may be
    useful in contexts where there is the possibility of executing
    notebooks with memory-consuming infinite loops.


NotebookClient.record_timing \: Bool
    Default: ``True``

    
    If `True` (default), then the execution timings of each cell will
    be stored in the metadata of the notebook.


NotebookClient.shell_timeout_interval \: Int
    Default: ``5``

    
    The time to wait (in seconds) for Shell output before retrying.
    This generally doesn't need to be set, but if one needs to check
    for dead kernels at a faster rate this can help.


NotebookClient.shutdown_kernel \: 'graceful'|'immediate'
    Default: ``'graceful'``

    
    If `graceful` (default), then the kernel is given time to clean
    up after executing all cells, e.g., to execute its `atexit` hooks.
    If `immediate`, then the kernel is signaled to immediately
    terminate.


NotebookClient.startup_timeout \: Int
    Default: ``60``

    
    The time to wait (in seconds) for the kernel to start.
    If kernel startup takes longer, a RuntimeError is
    raised.


NotebookClient.store_widget_state \: Bool
    Default: ``True``

    
    If `True` (default), then the state of the Jupyter widgets created
    at the kernel will be stored in the metadata of the notebook.


NotebookClient.timeout \: Int
    Default: ``None``

    
    The time to wait (in seconds) for output from executions.
    If a cell execution takes longer, a TimeoutError is raised.
    
    `None` or `-1` will disable the timeout. If `timeout_func` is set,
    it overrides `timeout`.


NotebookClient.timeout_func \: Any
    Default: ``None``

    
    A callable which, when given the cell source as input,
    returns the time to wait (in seconds) for output from cell
    executions. If a cell execution takes longer, a TimeoutError
    is raised.
    
    Returning `None` or `-1` will disable the timeout for the cell.
    Not setting `timeout_func` will cause the preprocessor to
    default to using the `timeout` trait for all cells. The
    `timeout_func` trait overrides `timeout` if it is not `None`.

