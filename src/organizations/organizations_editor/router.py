from fastapi import APIRouter, HTTPException
from src.organizations.models import OrganizationAdd, OrganizationGet
from src.weaviate_client import client

router = APIRouter(
    prefix="/organization/edit",
    tags=["Organizations Editor"]
)


@router.post("/create-organization/", response_model=OrganizationGet)
async def create_organization(organization: OrganizationAdd):
    organization_object = {
        "name": organization.name,
        "link": organization.link,
        "description": organization.description,
        "logo_link": organization.logo_link,
        "categories": organization.categories,
        "countries": organization.countries
    }

    if not organization.logo_link.startswith("data:image/"):
        raise HTTPException(status_code=422,
                            detail=" Invalid link, follow the format: data:image/"
                                   "png;base64,iVBORw0KGgoAAAANSUhEUgAAASwAAACoCAMAAABt9SM9AAAAb1BMVEX///"
                                   "8AkuYAjeUAieQAi+UAjuUAkOb6/f/v9v0Ah+Sgy/Ial+fI4Pfq9PwAk+b2+/"
                                   "7c7PqAvO+PwvCbyPJus+2t0fS31vUAg+PR5vnE3vddrOu62faQw/Dh7vtMpeqw0/"
                                   "Rkr+w4nuh2t+5Coukwm+hs64P0AAAJyklEQVR4nO2bbYOyKhCGE5DUzHLNVq00rf//"
                                   "G4/yoqiQtdn27GmuT2uLBDfDMAy0WAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                                   "AAAAAAAAAAAAAAAAPxBNi3vbsm/T/GNBd/Fu9vyz+MhS4C8d7flnwfEegAQ6wFArAcA"
                                   "sR4AxHoAEOsBQKwH8Dux/He3BfiD9HaAS/UB9oZD4m4HeFik3YOn7g33727lP0LUeaZ"
                                   "4sW8f7C9w8GOeEiv51aa+n2fE8r9z53db+2aeEYtalHxUVPGEWOxV95MSg0+Ixf/vf"
                                   "tBS+XOxYvF/d/vbbX4bfbFI+zAtVknl/3+7zW8jtQOBnSyS7mG/8LsHnRd3sCIscJt"
                                   "uylr4sf1QWq7CWZqwzoLdy7diTssPHxpCuxULRY98e+JSC2UzdGND6opWM1R0i24H6"
                                   "EYLT90BKnvDSN01FupGMea1ZK3LsqyHWlw1L7ozWARbYfCLdxGHbs0L710Nx96+VMTCjw"
                                   "Tyu+ZFsn6+H6xNr46KD6okPxer06p+1Y+j45e3v2eYP1GsXLEsC9XYNkIE55Mx6ieK"
                                   "ValidVBiTTT/E8XqPhkykSv8RLFObVA6BN8W4hPFWlwNWtGJGOpviaXsAIehg3FvqB"
                                   "GraAv3cU+3v/5vibUNVgKrjkMt+RDUe8P2wTos/O7BV//Ttk5vWuQ48fV/S6x5cLyV"
                                   "TqvpjcyfEWs5C852/1Vi7WpItFqt0yIuUqGPXqxtut/7tybwOvWOX1GhJM8MYiVRel/"
                                   "dG79txNo/7A+9IsvMxbNACLL1UZarydYkFcWkiVqxXSVasTbehZWo690NO8pxjisswl5"
                                   "USb20Ym0yjLA6YkUu6z736y5c4rLsxza0RBF8bseitLUdnA1KruPtzrbEna4Ul8lYrBAj"
                                   "2tURHMZahaoZU5w5RrEK0lSF2zoiotZtKQcGG7cZ3NpPl7jThboigbI1BkZPq1RT73QyjVW"
                                   "Ebt8EqRsOxPLRYD6TyyAjkdiDUaZ4rxfLyfkKjcQisw2GdZftlt9vitresIHfp+6/r4Be8qy"
                                   "K/OVYqkU5dmx8ArdiRe64PrvnX+JxCQtHOrFiIjouLOugqbtN6XA5Ru6EpK8V66pRiXOVTa"
                                   "G1S+g1S4p1lOZuI6UIUdx4jJU6kLQx1xmJtS5lB/GOfVBIrWhdeauKm6hiSWz57a7zUrFQb"
                                   "NIq512r/VDoFV4YkE4vIdZeKFGXKNLUOxNhiaidLYnoMUK7OPWL0OIlSDIUK5K+0aZ+/02c"
                                   "Hz3v6yJdEx5NNIqvYVx4VUCQKzqTvEgsYtLK419ILtLyk25WcrHWXCu0ar1dxD+hpXheCr27EdlTmWlVx"
                                   "TpdZdW46r9JIuEfnFCMTDAQC2dy2m/30jucXiOWbTp82PC2YfUcLZJziovFc2KkUkqsA/6ZEKdiXUYXxSEu"
                                   "c4xYblsR6yjNCgVyZPibtrpanHjd/DSqFQtrll/l7GpWXFMszk80cD9fU8h517yVsAfUV3sTsAKUt5"
                                   "lNJXsQ6SYH9p2tWNuVNCu3rWvN38x7Ly5XTC12GiXFMiTxXyKWOcfAGjM6UwxRJ9a5aTq9DErwuUmYy"
                                   "F9M8ED/BVKsUDpytOoWhlD7psMbFXViEZ1d1QSvEAubDu95ImjcT6sVa8lUGWe/jnY7CKzJpu0fE8s+"
                                   "SrOirrqF52Y9shqePVm1YhnHOtdvUZ7CbFgs7axZKfkViUastGkuPY9KCBEX0shMoQnvuAwm6FWNzra"
                                   "s7qHRLsRYNadRXCxiGuvwBdsdo2EtWE5Cc1bN/X4jFrMgpJkG7Eiy6QazTtt0hNtPbPdtmA9JHo4o2b"
                                   "f7UizDDK+dqzFr/mM0diFhmuhOX69SLL7v0Rw5MhUaFaObSZi+WP2mcGdn2SPYx43BM7FoZaibm+a8m"
                                   "E9XmQFpJ+lZ7g2ZW8CaEsygmg6xLhNT4qYVi7sXoq6qu5sup8n28r2h+eLB7GIhc1aUBSpaw9v1xNK"
                                   "FtCkSHQrvEovk/A81opsQKxJi3biHnc3t4Y0zXlpWrvkPNyhHNEd3AyeWlsW8GjEdc3OxaD1fI24Gbu"
                                   "f/DKeaAtefFiue2Wm5t07reUSj+Qdf1GWHdFKEbCFNhZc1doiJRc9NcF8J22or4+cwlGhx2zjrhlj"
                                   "recNSdPOWVWmQgm9Rr7Kzut0S3/CcbgQAnVhi7c+4524zP2wm091pq4MZ85RYC+0Rw0+h5tRMA/M3dDf6"
                                   "nHkTJlFiML4DzzQ1fzL7MIUnXCwxHPJSj5jVLA8q9kx6JsWK5pyHEwfPPI4ZdZTna3mKjQeVI9NiYTt"
                                   "f1CvthkjQE2vJN8ntCF7YVL5xy25SrDnnIdYfLXTwYsM1QN0mi632oKJM2alwaQ2Lbk+shcMNQW6dD"
                                   "9qxWib9tPLNXyXNt+OZPEuVi1WpfrbkuVPRRpEHwb2o88xfu6oNxr0v86ibb0ZiycsXSMx8Piqop9bBJd"
                                   "/S2KbFmi1bioyhb4cwoqBz8r6IH+VlcJGCwN1MlEk8ua6deEaBdD8S2mR1H+xyLJZMjRKe6EjH6TSWw"
                                   "xYnEneI1bvc+IxW91yglXldnB/YFd79RXgBtzUlkQixUejXRdb7TCTxurEQ6VaKd2ldwvFD3KbKh2L"
                                   "JJDXmu/cdlx0FHnOuTsyPelBxt1j+LF7rzsvGIlas40ZMKGlPB0mX42rvLdmkObyVJdSF9ozaSpoio"
                                   "oS71IjVBqfcC0rDQBitrrY8esTqgcXELynn8FrkfJdW9TTTzfpeFjnRDR5dqcdqmaYSVsdYLBmci"
                                   "iOaqybNguSmQhVrc9Cv7DMkl/H9V/41p4Juf2XYotHo9TLuNV+jSngLNGKJpVSm0cY64zbwU8TaH"
                                   "ONQvxmJn/XxrvHoS0Ni9UM7RIcJl02Oe3JRPFpnk5VyiNacrPGe8Xvwg+CAbxzkMX3RP+5GtNs9M"
                                   "pvmqu7XVWowgOypHKBNH/wRmGe3PaVEGyX6JZZHoBS5O92MOFwwsptbAjbCpTwCWTa/sCiHRQO7b"
                                   "mP3GFnCE1JEgp6HKlFdG7PhJD0VJud1fcJt4R/8jiStVrVnxnhVmeLY7deluZuDaRabfnnhFGF2"
                                   "uWRhoWi5zq7V6NLA5rw697JsSXQug6A8R8NRDks5MAfP6Og3wU/VsnVJ4Ltw1lM/wtis17rbEm9n"
                                   "s/rRTKTueBw/Ad1yPCUVzma42vgnifFjU9HG54lLyP9nnJ1791ykCIWfalWCdUjGAaFOKZz91K3/r"
                                   "zicyU3B6tjE3h0+0qtrSaLMxs3tY1WzJvirw56yKj7YURlwkvhY5WWA+Nbfuua7rzgFnQAAAAAAA"
                                   "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIC/wH/cuowGQA/7DgAAAABJRU5ErkJggg== ")

    result = client.data_object.create(
        data_object=organization_object,
        class_name="Organization"
    )

    object_id = result

    return OrganizationGet(
        id=object_id,
        name=organization.name,
        description=organization.description,
        logo_link=organization.logo_link,
        link=organization.link,
        countries=organization.countries,
        categories=organization.categories
    )


@router.delete("/delete-organization/{organization_id}", response_model=OrganizationGet)
async def delete_organization(organization_id: str):
    organization_object = client.data_object.get_by_id(
        organization_id,
        class_name="Organization"
    )
    client.data_object.delete(
        organization_id,
        class_name="Organization",
    )
    return OrganizationGet(id=organization_id, name=organization_object["properties"]["name"],
                   link=organization_object["properties"]["link"], description=organization_object["properties"]["description"],
                   logo_link=organization_object["properties"]["logo_link"],
                           categories=organization_object["properties"]["categories"],
                           countries=organization_object["properties"]["countries"])


@router.put("/edit-organization/{organization_id}", response_model=OrganizationGet)
async def edit_organization(organization: OrganizationAdd, organization_id: str):
    organization_object = {
        "name": organization.name,
        "link": organization.link,
        "description": organization.description,
        "logo_link": organization.logo_link,
        "categories": organization.categories,
        "countries": organization.countries,
    }

    result = client.data_object.replace(
        uuid=organization_id,
        class_name="Organization",
        data_object=organization_object
    )

    return OrganizationGet(
        id=organization_id,
        name=organization.name,
        link=organization.link,
        description=organization.description,
        logo_link=organization.logo_link,
        categories=organization.categories,
        countries=organization.countries

    )
