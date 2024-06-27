import sys
from lxml import etree
from saxonpy import PySaxonProcessor


def load_rules(rules_file):
    tree = etree.parse(rules_file)
    rules = tree.findall('.//rule')
    return {rule.get('name'): {
        'message': rule.find('message').text,
        'xpath': rule.find('xpath').text,
        'priority': int(rule.find('priority').text)
    } for rule in rules}


def lint_xslt(xslt_file, rules):
    with PySaxonProcessor(license=False) as proc:
        xslt_proc = proc.new_xslt30_processor()
        document = proc.parse_xml(xml_file_name=xslt_file)
        for name, rule in rules.items():
            xpath_expression = rule['xpath']
            violations = xslt_proc.evaluate_xpath(context_item=document, xpath_expression=xpath_expression)
            if violations:
                print(f"Rule '{name}' violated: {rule['message']}")
                for violation in violations:
                    print(f"  at {violation.node_name} line {violation.line_number}")


def main(xslt_file, rules_file):
    rules = load_rules(rules_file)
    lint_xslt(xslt_file, rules)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python xsl_linter.py <xslt_file> <rules_file>")
        sys.exit(1)

    xslt_file = sys.argv[1]
    rules_file = sys.argv[2]
    main(xslt_file, rules_file)
