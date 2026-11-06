from lab8_god_object import Lab8GodObject


god = Lab8GodObject()

god.register_user_and_task(
    name="Evelina",
    email="evelina@example.com",
    title="Lab 8 audit",
    priority="high",
)

print("===== SHOTGUN SURGERY FAIL =====")

# Після малої зміни сигнатури ReportService
# цей виклик у God Object більше не сумісний.
print(god.build_task_report())
