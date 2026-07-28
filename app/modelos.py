from dataclasses import dataclass, field
from typing import List


@dataclass
class Convocacao:
    cidade: str
    cargo: str
    nome: str
    edicao: str
    data: str
    trecho: str = ""


@dataclass
class ResultadoCidade:
    cidade: str
    nova_edicao: bool = False
    edicoes_analisadas: int = 0
    convocacoes: List[Convocacao] = field(default_factory=list)
    erros: List[str] = field(default_factory=list)

    @property
    def total_convocacoes(self):
        return len(self.convocacoes)


@dataclass
class ResumoExecucao:
    cidades: List[ResultadoCidade] = field(default_factory=list)

    @property
    def total_cidades(self):
        return len(self.cidades)

    @property
    def total_edicoes(self):
        return sum(c.edicoes_analisadas for c in self.cidades)

    @property
    def total_novas_edicoes(self):
        return sum(1 for c in self.cidades if c.nova_edicao)

    @property
    def total_convocacoes(self):
        return sum(c.total_convocacoes for c in self.cidades)

    @property
    def total_erros(self):
        return sum(len(c.erros) for c in self.cidades)