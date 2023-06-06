import pandas as pd
from unittest.mock import AsyncMock
from pytest_mock import MockerFixture
import pytest

from app.domain.usecases.parceiro.import_csv import ImportCsvUseCase
from app.application.ports.parceiro.parceiro_repository import AbstractParceiroRepository
from app.application.dtos.parceiro_dto import ParceiroDto
from app.domain.entities.parceiro.parceiro import Parceiro

# Sample CSV content for testing
csv_content = """CNPJ,Razão Social,Nome Fantasia,Telefone,Email,CEP\n16.470.954/0001-06,Sol Eterno,Sol Eterno LTDA,(21) 98207-9901,atendimento@soleterno.com,22783-115"""

# Sample dataframe that would result from reading the above CSV
df = pd.DataFrame({
    "CNPJ": ["16470954000106"],
    "Razão Social": ["Sol Eterno"],
    "Nome Fantasia": ["Sol Eterno LTDA"],
    "Telefone": ["21982079901"],
    "Email": ["atendimento@soleterno.com"],
    "CEP": ["22783115"],
    "Cidade": ["Rio de Janeiro"],
    "Estado": ["RJ"],
})

# Sample parceiro for testing
parceiro = Parceiro(
    cnpj="16470954000106",
    razao_social="Sol Eterno",
    nome_fantasia="Sol Eterno LTDA",
    telefone="21982079901",
    email="atendimento@soleterno.com",
    cep="22783115",
    cidade="Rio de Janeiro",
    estado="RJ",
)

# Sample ParceiroDto for testing
parceiro_dto = ParceiroDto(**parceiro.dict())

@pytest.mark.asyncio
async def test_import_csv(mocker: MockerFixture):
    # Mock the parceiro_repository
    parceiro_repository = mocker.MagicMock(AbstractParceiroRepository)

    # Mock the methods in parceiro_repository
    parceiro_repository.get_by_cnpj = mocker.MagicMock(return_value=parceiro)
    parceiro_repository.add = mocker.MagicMock(return_value=parceiro_dto)
    parceiro_repository.update = mocker.MagicMock(return_value=parceiro_dto)

    # Mock ViaCep's get_address method to return a dictionary
    mocker.patch(
        "app.infrastructure.integrations.via_cep.ViaCep.get_address",
        new_callable=AsyncMock, return_value={
            "cidade": "Rio de Janeiro", "estado": "RJ"
        },
    )

    # Initialize the use case
    use_case = ImportCsvUseCase(parceiro_repository)

    # Execute the use case
    result = await use_case.execute(csv_content)

    # Assert that the repository's methods were called with the right arguments
    parceiro_repository.get_by_cnpj.assert_called_with("16470954000106")
    parceiro_repository.add.assert_called_with(parceiro)
    #parceiro_repository.update.assert_called_with(parceiro)

    # Assert that the result is as expected
    expected_result = {"created": [parceiro_dto], "updated": []}
    assert result == expected_result
