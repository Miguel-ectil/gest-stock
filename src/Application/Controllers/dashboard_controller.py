from flask import jsonify, make_response
from src.Application.Service.dashboard_service import DashboardService

class DashboardController:
    @staticmethod
    def get_dashboard_data(current_user_id):
        try:
            dashboard_data = DashboardService.get_dashboard_data(current_user_id)
            
            return make_response(jsonify({
                "dashboard": dashboard_data
            }), 200)
            
        except Exception as e:
            print(f"Erro ao buscar dados do dashboard: {str(e)}")
            return make_response(jsonify({"erro": "Falha ao carregar dados do dashboard"}), 500)