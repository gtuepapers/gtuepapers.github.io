const serverUrl = "http://34.100.217.114:8080/"

const searchBtn = document.querySelector("#search_btn")
const searchInp = document.querySelector("#search_inp")
const searchForm = document.querySelector("#search_frm")
const formErrField = document.querySelector("#form_err")

const searchResultTemplate = `
<hr>
<div class="container bounce animated ">
    <!-- Start: Intro -->
    <div class="intro">
        <h2 class="text-center">Papers [ $1 ]</h2>
        <p class="text-center"></p>
    </div>
    <!-- End: Intro -->
    <!-- Start: Features -->
    <div id="searchResult" class="row justify-content-center bounce animated features features" style="padding-bottom: 20px;">
        
    </div>
</div>`

const searchResultItemTemplate = `
<div class="col-sm-6 col-md-5 col-lg-4 item ">
<div class="box hover_pointer search_item" onclick="downloadSinglePaper(this)" data-url="$2" data-code="$3">
    <h3 class="name">$1</h3>
</div>
</div>`

const searchResultAllDownloadButtonTemplate = `
<button class="btn btn-primary" type="button" onClick="downloadAllPapers(this)" data-codes="$1" data-name="$2"
    style="margin: 20px;margin-top: 0px;margin-bottom: 30px;margin-right: 30ox;margin-left: 35px;">Download
    All [ $1.zip ]</button>`

/**
 * Downloads Single Paper
 * @param {HTMLElement} element 
 */
async function downloadSinglePaper(element) {
    $("#download_modal").modal("show")
    let paperUrl = element.getAttribute("data-url")
    let paperCode = element.getAttribute("data-code")
    let downloadUrl = serverUrl + "pdf/" + paperCode + "?url=" + paperUrl
    let data = await (await httpRequest(downloadUrl)).blob()
    let link = document.createElement('a');
    link.href = (URL || webkitURL).createObjectURL(data, { type: "application/pdf" });
    link.download = paperCode + '.pdf';
    link.dispatchEvent(new MouseEvent('click'));
    $("#download_modal").modal("hide")
}

async function downloadAllPapers(element) {
    $("#download_modal").modal("show")
    let paperCode = element.getAttribute("data-codes")
    let paperName = element.getAttribute("data-name")
    let downloadUrl = serverUrl + "pdfbundle/" + paperName + "?codes=" + paperCode
    let data = await (await httpRequest(downloadUrl)).blob()
    let link = document.createElement('a');
    link.href = (URL || webkitURL).createObjectURL(data, { type: "application/zip" });
    link.download = paperName + '.zip';
    link.dispatchEvent(new MouseEvent('click'));
    $("#download_modal").modal("hide")
}

async function httpRequest(url) {
    console.log("Requesting to ", url)
    let response = await fetch(url)
    return response
}

function getNameFromUrl(url) {
    let isNewerVersion = url.includes("uploads");
    let urlSplit = url.split("/")
    let batch = urlSplit[urlSplit.length - (isNewerVersion ? 3 : 2)]
    let name = ""
    if (batch[0] == "W") {
        name = "Winter "
    } else {
        name = "Summer "
    }
    name += batch.substring(batch.length - 4)
    return name
}

// search
searchInp.addEventListener("input", (event) => {
    formErrField.style.display = "none"
})

searchForm.addEventListener("submit", async (event) => {
    try {
        event.preventDefault()

        let tempSearchResultBox = document.querySelector("#searchResultBox")
        tempSearchResultBox?.remove()

        let code = searchInp.value
        let searchUrl = serverUrl + "search/" + code
        papers = await (await httpRequest(searchUrl)).json()
        console.log(papers)
        if (papers.length == 0) {
            throw new Error("No paper with code: " + code + " found!")
        }
        let searchResultDiv = document.createElement("div")
        searchResultDiv.id = "searchResultBox"
        searchResultDiv.classList.add("features-boxed")
        searchResultDiv.innerHTML = searchResultTemplate.replace("$1", code)
        searchForm.parentElement.parentElement.after(searchResultDiv)

        let searchResult = document.querySelector("#searchResult")
        papers.forEach(paperUrl => {
            searchResult.innerHTML += searchResultItemTemplate
                .replace("$1", getNameFromUrl(paperUrl))
                .replace("$2", paperUrl)
                .replace("$3", code)
        });
        searchResult.parentElement.innerHTML += searchResultAllDownloadButtonTemplate
            .replace(/\$1/g, code)
            .replace("$2", code)

        searchResult.scrollIntoView()
    } catch (err) {
        formErrField.innerHTML = err.message
        formErrField.style.display = "block"
    }
})


// all papers
const showcase = document.querySelector("#all_papers_showcase")
const levels = ["departments"]

const paperShowcaseTemplate = `<div class="col-sm-6 col-md-5 col-lg-4 item">
<div class="box box hover_pointer search_item" onclick="paperShowCase(this)" data-json="$2">
    <h3 class="name">$1</h3>
</div>
</div>`
const paperShowcaseCodeTemplate = `<div class="col-sm-6 col-md-5 col-lg-4 item">
<div class="box box hover_pointer search_item" onclick="downloadSinglePaper(this)" data-url="$2" data-code="$3">
    <h3 class="name">$1</h3>
</div>
</div>`
const allPaperDownloadAllButtonTemplate = `<button id="all_paper_download_btn" class="btn btn-primary" type="button" onClick="downloadAllPapers(this)" data-codes="$1" data-name="$2"
style="margin: 20px;margin-top: 0px;margin-bottom: 30px;margin-right: 30ox;margin-left: 35px;">Download
All [ $2.zip ]</button>`

const paperLevelShower = document.querySelector("#all_paper_levels");
console.log(paperLevelShower)
paperLevelShower.style.display = "none";

paperLevelShower.addEventListener("click", (event) => {
    console.log("here")
    levels.pop()
    if (levels.length <= 1) {
        paperLevelShower.style.display = "none";
    }
    showcaseAllPapers(levels[levels.length - 1])
})

async function showcaseAllPapers(jsonFile) {
    const showcase = document.querySelector("#all_papers_showcase")
    document.querySelector("#all_paper_download_btn")?.remove()
    showcase.innerHTML = "Loading ..."
    jsonFileUrl = serverUrl + "json/" + jsonFile + ".json"
    json = await (await httpRequest(jsonFileUrl)).json()
    json.sort()
    showcase.innerHTML = ""
    json.forEach(subcat => {
        showcase.innerHTML += paperShowcaseTemplate
            .replace("$1", subcat)
            .replace("$2", jsonFile.includes("sem") ? ("code:" + subcat) : ((jsonFile == "departments" ? "" : jsonFile + "-") + subcat))
    })

    if (jsonFile.includes("sem")) {
        showcase.parentElement.innerHTML += allPaperDownloadAllButtonTemplate
            .replace("$1", json.join(","))
            .replace(/\$2/g, jsonFile)
    }
    if (jsonFile != "departments")
        showcase.scrollIntoView()
}

async function showcaseAllPapersOfCode(code) {
    const showcase = document.querySelector("#all_papers_showcase")
    showcase.innerHTML = "Loading ..."
    document.querySelector("#all_paper_download_btn")?.remove()
    jsonFileUrl = serverUrl + "search/" + code
    json = await (await httpRequest(jsonFileUrl)).json()
    showcase.innerHTML = ""
    json.sort()
    json.forEach(url => {
        showcase.innerHTML += paperShowcaseCodeTemplate
            .replace("$1", getNameFromUrl(url))
            .replace("$2", url)
            .replace("$3", code)
    })
    if (json.length > 1)
        showcase.parentElement.innerHTML += allPaperDownloadAllButtonTemplate
            .replace("$1", code)
            .replace(/\$2/g, code)
    showcase.scrollIntoView()

}

function showNextLevel(nextLevel) {
    if (nextLevel.includes("code:")) {
        code = nextLevel.split(":")[1]
        levels.push(code)
        showcaseAllPapersOfCode(code)
        paperLevelShower.style.display = "block";
    } else {
        levels.push(nextLevel)
        showcaseAllPapers(nextLevel)
        paperLevelShower.style.display = "block";
    }
}

function paperShowCase(element) {
    nextLevel = element.getAttribute("data-json")
    showNextLevel(nextLevel)
}

showcaseAllPapers(levels[0])
