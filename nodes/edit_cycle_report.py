from pocketflow import Node

class EditCycleReportNode(Node):
    def prep(self, shared):
        return shared.get("quality_control", {}).get("deadly_sins_violations", {}), shared.get("content_pieces", {})

    def exec(self, inputs):
        violations, content = inputs
        report = "Maximum edit cycles reached. Manual review required.\n\n"
        report += "Persistent violations:\n"
        for platform, platform_violations in violations.items():
            for sin, sin_data in platform_violations.items():
                if sin_data.get("count", 0) > 0:
                    report += f"- {platform}: {sin} (count: {sin_data['count']})\n"
        return report

    def post(self, shared, prep_res, exec_res):
        shared["manual_review_report"] = exec_res
        return "default"
