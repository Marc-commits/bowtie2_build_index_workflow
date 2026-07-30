configfile: "config/config.yaml"


include: "workflow/rules/build_index.smk"


rule bowtie2_build_index_workflow_all:
    """Convenience aggregate target for standalone runs/tests of this module.
    Consuming workflows typically depend on the bowtie2_build output
    directly instead of this aggregate rule.
    """
    input:
        multiext(
            config["index_name"],
            ".1.bt2",
            ".2.bt2",
            ".3.bt2",
            ".4.bt2",
            ".rev.1.bt2",
            ".rev.2.bt2",
        ),
    default_target: True
