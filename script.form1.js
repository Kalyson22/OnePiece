const KEY_BD = '@OnePiece'

let listaArcos = {
    ultimoID : 0,
    arcos :[]
}

function gravarBD(){
    localStorage.setItem(KEY_BD, JSON.stringify(listaArcos));
}

function lerBD(){
    const data = localStorage.getItem(KEY_BD)
    if(data){
        listaArcos = JSON.parse(data);
    }
    desenhar();
}


function desenhar(){
    debugger;
    const tbody = document.getElementById("listaArcosBody")
    if(tbody){
        tbody.innerHTML = listaArcos.arcos
        .sort((a, b) => {
            return a.nomeArco < b.nomeArco ? -1: 1
           
        })
        .map(arcos =>{

            return `<tr>
                        <td>${arcos.id}</td>
                        <td>${arcos.nomeArco}</td>
                        <td>${arcos.episodios}</td>
                        <td>${arcos.ano}</td>
                        <td>${empresas.descricao}</td>
                        <td>
                            <button onclick='vizualizar("cadastro", false ,${arcos.id})'>Editar</button>
                            <button class="vermelho" onclick="perguntaExcluir(${arcos.id})">Excluir</button>
                        </td>
                    <tr/>`
        }) .join('')
    }
}
function salvar(nomeArco, episodios, ano, descricao){
    const id = listaArcos.ultimoID + 1;
    listaArcos.ultimoID =  id;
    listaArcos.arcos.push({
        id, nomeArco, episodios, ano, descricao
    })
    gravarBD();
    desenhar();
    vizualizar("lista");
}

function editar(id, nomeArco, episodios, ano, descricao){
    let arco = listaArcos.arcos.find(arco => arco.id == id)
    arco.nomeArco = nomeArco
    arco.episodios =episodios
    arco.ano = ano
    arco.descricao = descricao
    gravarBD();
    desenhar();
    vizualizar("lista");
}

function deletar(id){
    listaArcos.arco =listaArcos.arcos.filter(arco => {
        return arco.id != id
    })
    desenhar();
    gravarBD();

}

function perguntaExcluir(id){
    if(confirm('Que deletar esse resgistro?')){
        deletar(id);
        desenhar();
    }

}

function limparEdicao(){
    document.getElementById("nomeArco").value = ''
    document.getElementById("episodios").value= ''
    document.getElementById("ano").value= ''
    document.getElementById("descricao").value= ''
}

function vizualizar(pagina, novo=false, id=null){
    document.body.setAttribute('page', pagina)
    if (pagina = 'cadastros'){
        if(novo) limparEdicao();
        if(id){
            const arco =listaArcos.arcos.find(arco => arco.id == id)
            if(empresa){
                document.getElementById("id").value = arco.id
                document.getElementById("nomeArco").value = arco.nomeArco
                document.getElementById("episodios").value= arco.episodios
                document.getElementById("ano").value= arco.ano
                document.getElementById("descricao").value= arco.descicao
            }
        }
        document.getElementById("nomeArco").focus();
    }
}

function submeter(e){
    e.preventDefault()
    const data = {
        id:document.getElementById("id").value,
        nomeArco:document.getElementById("nomeArco")value,
        episodios:document.getElementById("episodios").value,
        ano:document.getElementById("ano").value,
        descricao:document.getElementById("descricao").value,
    }
    if (data.id){
        editar(data.id, data.nomeArco, data.episodios, data.ano, data.descricao)
    }else{
        salvar(data.id, data.nomeArco, data.episodios, data.ano, data.descricao)
    }
}

window.addEventListener('load', () =>{
    lerBD();
    document.getElementById("cadastroRegistros").addEventListener('submit', submeter)
})