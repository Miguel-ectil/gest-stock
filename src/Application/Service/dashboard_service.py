from src.Infrastructure.Model.venda import Venda
from src.Infrastructure.Model.produto import Produto
from src.Infrastructure.Model.user import User
from src.config.data_base import db
from sqlalchemy import func, extract, case
from datetime import datetime, timedelta
import calendar

class DashboardService:
    @staticmethod
    def get_dashboard_data(user_id):
        try:
            user_id = int(user_id)
            hoje = datetime.now()
            
            # Períodos para comparação
            primeiro_dia_mes = hoje.replace(day=1)
            primeiro_dia_ano = hoje.replace(month=1, day=1)
            mes_anterior = hoje.replace(day=1) - timedelta(days=1)
            primeiro_dia_mes_anterior = mes_anterior.replace(day=1)
            ultimo_dia_mes_anterior = mes_anterior
            
            # 1. MÉTRICAS PRINCIPAIS DE VENDAS
            # Vendas do mês atual
            vendas_mes_atual = db.session.query(
                func.sum(Venda.quantidade * Venda.preco_unitario)
            ).filter(
                Venda.id_vendedor == user_id,
                extract('year', Venda.data_venda) == hoje.year,
                extract('month', Venda.data_venda) == hoje.month
            ).scalar() or 0.0
            
            # Vendas do mês anterior
            vendas_mes_anterior = db.session.query(
                func.sum(Venda.quantidade * Venda.preco_unitario)
            ).filter(
                Venda.id_vendedor == user_id,
                extract('year', Venda.data_venda) == mes_anterior.year,
                extract('month', Venda.data_venda) == mes_anterior.month
            ).scalar() or 0.0
            
            # Crescimento mensal
            crescimento_mensal = 0
            if vendas_mes_anterior > 0:
                crescimento_mensal = ((vendas_mes_atual - vendas_mes_anterior) / vendas_mes_anterior) * 100
            
            # 2. LUCROS E RECEITAS
            # Lucro anual
            lucro_anual = db.session.query(
                func.sum(Venda.quantidade * Venda.preco_unitario)
            ).filter(
                Venda.id_vendedor == user_id,
                extract('year', Venda.data_venda) == hoje.year
            ).scalar() or 0.0
            
            # Lucro mensal
            lucro_mensal = float(vendas_mes_atual)
            
            # Ticket médio
            total_vendas_mes = Venda.query.filter(
                Venda.id_vendedor == user_id,
                extract('year', Venda.data_venda) == hoje.year,
                extract('month', Venda.data_venda) == hoje.month
            ).count()
            
            ticket_medio = lucro_mensal / total_vendas_mes if total_vendas_mes > 0 else 0
            
            # 3. PRODUTOS
            # Produto mais vendido
            produto_mais_vendido = db.session.query(
                Produto.name,
                func.sum(Venda.quantidade).label('total_vendido')
            ).join(Venda, Venda.id_produto == Produto.id_produto
            ).filter(Venda.id_vendedor == user_id
            ).group_by(Produto.id_produto, Produto.name
            ).order_by(func.sum(Venda.quantidade).desc()
            ).first()
            
            produto_nome = produto_mais_vendido[0] if produto_mais_vendido else "Nenhum"
            total_vendido_produto = int(produto_mais_vendido[1]) if produto_mais_vendido else 0
            
            # Total de produtos ativos
            total_produtos_ativos = Produto.query.filter(
                Produto.id_vendedor == user_id,
                Produto.status == True
            ).count()
            
            # 4. ESTOQUE
            # Produtos com estoque baixo
            estoque_baixo = Produto.query.filter(
                Produto.id_vendedor == user_id,
                Produto.quantidade < 10,
                Produto.status == True
            ).count()
            
            # Valor total em estoque
            valor_estoque = db.session.query(
                func.sum(Produto.quantidade * Produto.preco)
            ).filter(
                Produto.id_vendedor == user_id,
                Produto.status == True
            ).scalar() or 0.0
            
            # 5. PERDAS E INATIVOS
            perdas_anuais = db.session.query(
                func.sum(Produto.quantidade * Produto.preco)
            ).filter(
                Produto.id_vendedor == user_id,
                Produto.status == False,
                Produto.quantidade > 0
            ).scalar() or 0.0
            
            # 6. VENDAS POR MÊS (últimos 12 meses)
            doze_meses_atras = hoje - timedelta(days=365)
            vendas_por_mes = db.session.query(
                extract('month', Venda.data_venda).label('mes'),
                extract('year', Venda.data_venda).label('ano'),
                func.sum(Venda.quantidade * Venda.preco_unitario).label('total')
            ).filter(
                Venda.id_vendedor == user_id,
                Venda.data_venda >= doze_meses_atras
            ).group_by('ano', 'mes'
            ).order_by('ano', 'mes'
            ).all()
            
            vendas_mensais_formatadas = []
            for venda in vendas_por_mes:
                vendas_mensais_formatadas.append({
                    "mes": int(venda.mes),
                    "ano": int(venda.ano),
                    "total": float(venda.total) if venda.total else 0.0,
                    "mes_nome": calendar.month_name[int(venda.mes)]
                })
            
            # 7. CATEGORIAS MAIS VENDIDAS
            categorias_mais_vendidas = db.session.query(
                Produto.categoria,
                func.sum(Venda.quantidade * Venda.preco_unitario).label('total_vendido')
            ).join(Venda, Venda.id_produto == Produto.id_produto
            ).filter(
                Venda.id_vendedor == user_id,
                Produto.categoria.isnot(None)
            ).group_by(Produto.categoria
            ).order_by(func.sum(Venda.quantidade * Venda.preco_unitario).desc()
            ).limit(5).all()
            
            categorias_formatadas = [{
                "categoria": cat[0] or "Sem categoria",
                "total_vendido": float(cat[1]) if cat[1] else 0.0
            } for cat in categorias_mais_vendidas]
            
            # 8. DESEMPENHO DIÁRIO (últimos 7 dias)
            sete_dias_atras = hoje - timedelta(days=7)
            vendas_ultimos_7_dias = db.session.query(
                func.date(Venda.data_venda).label('data'),
                func.sum(Venda.quantidade * Venda.preco_unitario).label('total')
            ).filter(
                Venda.id_vendedor == user_id,
                Venda.data_venda >= sete_dias_atras
            ).group_by(func.date(Venda.data_venda)
            ).order_by(func.date(Venda.data_venda)
            ).all()
            
            vendas_diarias_formatadas = []
            for i in range(7):
                data = hoje - timedelta(days=i)
                vendas_do_dia = next((v for v in vendas_ultimos_7_dias if v.data == data.date()), None)
                vendas_diarias_formatadas.insert(0, {
                    "data": data.strftime('%d/%m'),
                    "total": float(vendas_do_dia.total) if vendas_do_dia else 0.0
                })
            
            return {
                # Métricas principais
                "lucro_anual": float(lucro_anual),
                "lucro_mensal": float(lucro_mensal),
                "crescimento_mensal": round(crescimento_mensal, 2),
                "ticket_medio": round(float(ticket_medio), 2),
                
                # Produtos
                "produto_mais_vendido": produto_nome,
                "total_vendas_produto_mais_vendido": total_vendido_produto,
                "total_produtos_ativos": total_produtos_ativos,
                
                # Estoque
                "estoque_baixo": estoque_baixo,
                "valor_total_estoque": float(valor_estoque),
                
                # Perdas
                "perdas_anuais": float(perdas_anuais),
                
                # Totais
                "total_vendas_mes": total_vendas_mes,
                "total_vendas_ano": Venda.query.filter(
                    Venda.id_vendedor == user_id,
                    extract('year', Venda.data_venda) == hoje.year
                ).count(),
                
                # Gráficos e análises
                "vendas_por_mes": vendas_mensais_formatadas,
                "categorias_mais_vendidas": categorias_formatadas,
                "vendas_ultimos_7_dias": vendas_diarias_formatadas,
                
                # Status do negócio
                "status_negocio": "Excelente" if crescimento_mensal > 20 else 
                                "Bom" if crescimento_mensal > 0 else 
                                "Estável" if crescimento_mensal == 0 else "Atenção"
            }
            
        except Exception as e:
            print(f"Erro no dashboard service: {str(e)}")
            raise e